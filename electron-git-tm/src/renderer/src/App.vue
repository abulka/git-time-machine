<script setup lang="ts">
import Versions from './components/Versions.vue'
import AndyQDialog from './components/AndyQDialog.vue'
</script>

<template>
  <Versions></Versions>
  <Versions></Versions>

  <AndyQDialog>
    <template #content> extra content </template>
    <template #actions> extra stuff </template>
  </AndyQDialog>

  <p class="bg-green text-red">HI THERE TAILWIND</p>
  <div class="w-20">This element has a width of 20px.</div>
  <div class="border-4 border-red-500">This element has a thick red border.</div>
  <div class="text-xl">This text is larger.</div>
  <div class="text-center">This text is centered horizontally.</div>
  <div class="max-w-screen w-full text-xs pt-5">
    This element is full width on small screens, and is constrained to the screen width on larger
    screens. Hippocampes les sans je ce porteurs en de, les courants brides sillage des des qu'on
    des dispersant marées. D'or éclairs ma inouies quand leurs aux et clapotements lactescent,
    lorsqu'a hiver tout houle oiseau je. Restais vu repeché verte femme. Sans qu'une la je une
    maritimes l'eau énormes glauques. Des morves peaux ayant les couleurs en, braises ô blonds les
    ces aux. Moi d'oiseaux le pôles les au pour, brumes porteurs qu'aux des lors, du brumes fileur
    plus pôles arbres victimes au des, par zones les avaient frissons fientes des délirants. m'ont
    éternels de fond.
  </div>

  <div class="container mx-auto bg-gray-200 rounded-xl shadow border p-8 m-10">
    <p class="text-3xl text-gray-700 font-bold mb-5">Welcome!</p>
    <p class="text-gray-500 text-lg">Vue and Tailwind CSS in action</p>
  </div>

  <svg class="hero-logo" viewBox="0 0 900 300">
    <use xlink:href="./assets/icons.svg#electron" />
  </svg>
  <h2 class="hero-text">You've successfully created an Electron project with Vue and TypeScript</h2>
  <p class="hero-tagline">Please try pressing <code>F12</code> to open the devTool</p>

  <div class="links">
    <div class="link-item">
      <a target="_blank" href="https://evite.netlify.app">Documentation</a>
    </div>
    <div class="link-item link-dot">•</div>
    <div class="link-item">
      <a target="_blank" href="https://github.com/alex8088/electron-vite">Getting Help</a>
    </div>
    <div class="link-item link-dot">•</div>
    <div class="link-item">
      <a
        target="_blank"
        href="https://github.com/alex8088/quick-start/tree/master/packages/create-electron"
      >
        create-electron
      </a>
    </div>
  </div>

  <div class="features">
    <div class="feature-item">
      <article>
        <h2 class="title">Configuring</h2>
        <p class="detail">
          Config with <span>electron.vite.config.ts</span> and refer to the
          <a target="_blank" href="https://evite.netlify.app/config/">config guide</a>.
        </p>
      </article>
    </div>
    <div class="feature-item">
      <article>
        <h2 class="title">HMR</h2>
        <p class="detail">
          Edit <span>src/renderer</span> files to test HMR. See
          <a target="_blank" href="https://evite.netlify.app/guide/hmr-in-renderer.html">docs</a>.
        </p>
      </article>
    </div>
    <div class="feature-item">
      <article>
        <h2 class="title">Hot Reloading</h2>
        <p class="detail">
          Run <span>'electron-vite dev --watch'</span> to enable. See
          <a target="_blank" href="https://evite.netlify.app/guide/hot-reloading.html">docs</a>.
        </p>
      </article>
    </div>
    <div class="feature-item">
      <article>
        <h2 class="title">Debugging</h2>
        <p class="detail">
          Check out <span>.vscode/launch.json</span>. See
          <a target="_blank" href="https://evite.netlify.app/guide/debugging.html">docs</a>.
        </p>
      </article>
    </div>
    <div class="feature-item">
      <article>
        <h2 class="title">Source Code Protection</h2>
        <p class="detail">
          Supported via built-in plugin <span>bytecodePlugin</span>. See
          <a target="_blank" href="https://evite.netlify.app/guide/source-code-protection.html">
            docs
          </a>
          .
        </p>
      </article>
    </div>
    <div class="feature-item">
      <article>
        <h2 class="title">Packaging</h2>
        <p class="detail">
          Use
          <a target="_blank" href="https://www.electron.build">electron-builder</a>
          and pre-configured to pack your app.
        </p>
      </article>
    </div>
  </div>
</template>

<style lang="less">
@import './assets/css/styles.less';
</style>
