// Cynor - escena 3D del hero: un núcleo de cristal que "piensa", tres órbitas
// (atraer, atender, cerrar) y partículas que fluyen hacia el centro como clientes.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const host = document.querySelector('[data-hero3d]');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function start() {
  const canvas = document.createElement('canvas');
  canvas.className = 'hero3d__canvas';
  host.appendChild(canvas);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.6));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 0.9;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  camera.position.set(0, 0, 11);

  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.55;

  const world = new THREE.Group();
  scene.add(world);

  // Núcleo: esfera de cristal iridiscente que ondula lentamente
  const uniforms = { uTime: { value: 0 } };
  const coreMat = new THREE.MeshPhysicalMaterial({
    color: 0xa89bea, roughness: 0.12, metalness: 0.05,
    clearcoat: 1, clearcoatRoughness: 0.08,
    iridescence: 1, iridescenceIOR: 1.35, iridescenceThicknessRange: [180, 620],
    sheen: 0.6, sheenColor: new THREE.Color(0xe2f06c), sheenRoughness: 0.4,
  });
  coreMat.onBeforeCompile = (shader) => {
    shader.uniforms.uTime = uniforms.uTime;
    shader.vertexShader = 'uniform float uTime;\n' + shader.vertexShader.replace(
      '#include <begin_vertex>',
      `#include <begin_vertex>
       float w = sin(position.x * 2.6 + uTime * 0.9) + sin(position.y * 3.1 + uTime * 1.1) + sin(position.z * 2.2 + uTime * 0.7);
       transformed += normal * w * 0.045;`
    );
  };
  const core = new THREE.Mesh(new THREE.IcosahedronGeometry(1.25, 48), coreMat);
  world.add(core);

  // Brillo interior
  const glow = new THREE.Mesh(
    new THREE.SphereGeometry(0.62, 48, 48),
    new THREE.MeshBasicMaterial({ color: 0xa89bea, transparent: true, opacity: 0.45 })
  );
  world.add(glow);

  // Tres órbitas
  const ringDefs = [
    { r: 2.05, tilt: [1.15, 0.2, 0], color: 0xc9c0f4, speed: 0.12 },
    { r: 2.6, tilt: [0.55, -0.7, 0.3], color: 0xa89bea, speed: -0.09 },
    { r: 3.15, tilt: [1.9, 0.5, -0.4], color: 0xe2f06c, speed: 0.06 },
  ];
  const rings = ringDefs.map((d) => {
    const g = new THREE.Group();
    g.rotation.set(...d.tilt);
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(d.r, 0.008, 12, 320),
      new THREE.MeshBasicMaterial({ color: d.color, transparent: true, opacity: 0.55 })
    );
    g.add(ring);
    // un "satélite" por órbita
    const sat = new THREE.Mesh(
      new THREE.SphereGeometry(0.075, 24, 24),
      new THREE.MeshBasicMaterial({ color: d.color })
    );
    sat.position.x = d.r;
    g.add(sat);
    world.add(g);
    return { g, d };
  });

  // Partículas: clientes que entran en espiral hacia el núcleo
  const N = window.innerWidth < 700 ? 700 : 1500;
  const pos = new Float32Array(N * 3);
  const col = new Float32Array(N * 3);
  const p = [];
  const cA = new THREE.Color(0xffffff), cB = new THREE.Color(0xa89bea), cC = new THREE.Color(0xe2f06c);
  for (let i = 0; i < N; i++) {
    p.push({
      r: 1.6 + Math.random() * 4.6,
      a: Math.random() * Math.PI * 2,
      inc: (Math.random() - 0.5) * 1.6,
      s: 0.08 + Math.random() * 0.22,
      fall: 0.05 + Math.random() * 0.18,
      y: (Math.random() - 0.5) * 0.6,
    });
    const c = Math.random() < 0.08 ? cC : (Math.random() < 0.5 ? cA : cB);
    col.set([c.r, c.g, c.b], i * 3);
  }
  const pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  pGeo.setAttribute('color', new THREE.BufferAttribute(col, 3));
  const dot = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 64;
    const x = c.getContext('2d');
    const gr = x.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.35, 'rgba(255,255,255,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    x.fillStyle = gr; x.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(c);
  })();
  const points = new THREE.Points(pGeo, new THREE.PointsMaterial({
    size: 0.07, map: dot, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  }));
  world.add(points);

  // Luces de acento (se notan en el cristal)
  const l1 = new THREE.PointLight(0xa89bea, 40, 20); l1.position.set(-4, 3, 4); scene.add(l1);
  const l2 = new THREE.PointLight(0xe2f06c, 14, 20); l2.position.set(4, -3, 2); scene.add(l2);

  // Postproceso: brillo cinematográfico
  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.55, 0.6, 0.32);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());

  // Tamaño y encuadre: a la derecha en escritorio, centrado y abajo en celular
  function resize() {
    const w = host.clientWidth, h = host.clientHeight;
    renderer.setSize(w, h, false);
    composer.setSize(w, h);
    bloom.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    const wide = w / h > 1.15;
    world.position.set(wide ? 2.7 : 0, wide ? -0.1 : -3.1, 0);
    world.scale.setScalar(wide ? 0.88 : 0.66);
  }
  resize();
  window.addEventListener('resize', resize);

  // Mouse y scroll
  const target = { x: 0, y: 0 }, cur = { x: 0, y: 0 };
  host.closest('.cine-hero').addEventListener('pointermove', (e) => {
    const r = host.getBoundingClientRect();
    target.x = ((e.clientX - r.left) / r.width - 0.5) * 2;
    target.y = ((e.clientY - r.top) / r.height - 0.5) * 2;
  });

  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) loop(); }).observe(host);

  const clock = new THREE.Clock();
  let raf = 0;
  function frame() {
    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.elapsedTime;
    uniforms.uTime.value = t;

    cur.x += (target.x - cur.x) * 0.04;
    cur.y += (target.y - cur.y) * 0.04;
    const scroll = Math.min(1, window.scrollY / Math.max(1, host.clientHeight));
    world.rotation.y = t * 0.08 + cur.x * 0.35 + scroll * 1.2;
    world.rotation.x = cur.y * 0.22 + scroll * 0.35;
    camera.position.z = 11 + scroll * 3;

    core.rotation.y = t * 0.15;
    glow.scale.setScalar(1 + Math.sin(t * 1.6) * 0.06);
    rings.forEach(({ g, d }) => { g.rotation.z += d.speed * dt * 2; });

    for (let i = 0; i < N; i++) {
      const q = p[i];
      q.a += q.s * dt * (3 / q.r);
      q.r -= q.fall * dt;
      if (q.r < 1.35) { q.r = 5.6 + Math.random() * 0.8; q.a = Math.random() * Math.PI * 2; }
      const x = Math.cos(q.a) * q.r, z = Math.sin(q.a) * q.r;
      pos[i * 3] = x;
      pos[i * 3 + 1] = z * Math.sin(q.inc) * 0.5 + q.y;
      pos[i * 3 + 2] = z * Math.cos(q.inc);
    }
    pGeo.attributes.position.needsUpdate = true;

    composer.render();
  }
  function loop() {
    cancelAnimationFrame(raf);
    if (!visible) return;
    frame();
    if (!reduceMotion) raf = requestAnimationFrame(loop);
  }
  loop();
  host.classList.add('is-ready');
}

if (host) {
  try { start(); } catch (err) { host.classList.add('is-fallback'); console.warn('hero3d', err); }
}
