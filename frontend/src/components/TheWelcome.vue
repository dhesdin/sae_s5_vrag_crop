<script setup lang="ts">
import ConversationContainer from './ConversationContainer.vue'
import Header from "@/components/Header.component.vue"
import Help from './HelpCenter.vue'

import { useGlobalVarStore } from "@/stores/globabVar.store"
import { storeToRefs } from "pinia"
import InputSearchComponent from './InputSearch.component.vue'

const globalVarStore = useGlobalVarStore()
const { showConversation } = storeToRefs(globalVarStore)


</script>

<template>
  <div class="window" :class="{ 'is-searching': showConversation }">
    <Header />

    <main class="workspace">
      <section id="welcome-wrap" aria-labelledby="page-title">
      <div id="left-container" class="container">
        <h1 id="page-title" class="title">Décrivez une image.<br /><em>Retrouvez-la.</em></h1>
        <p class="intro">Aspect vous aide à retrouver les images dont vous avez besoin.</p>
        <InputSearchComponent id="input-search-container" />

      </div>

      <div id="right-container" class="container visual-panel" aria-label="Aperçu de l'analyse d'image">
        <div class="visual-panel__label">01 / Analyse</div>
        <img src="../assets/icon.svg" alt="" />
        <div class="visual-panel__caption">
          <strong>Projet réalisé par</strong>
          <span>Dhesdin Valentin | Gobfert Frédéric | Levitre Mathys</span>
        </div>
        <div class="visual-panel__stamp">V-CROP<br />RAG</div>
      </div>
      </section>
      <ConversationContainer
        id="conversation-container"
        :class="{ 'show-conversation': showConversation }"
      />
    </main>

    <Help />
  </div>
</template>

<style lang="css" scoped>

#welcome-wrap {
  min-height: 660px;
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(300px, .9fr);
  align-items: center;
  gap: clamp(3rem, 8vw, 9rem);
}

.workspace {
  width: min(1180px, calc(100% - 64px));
  min-height: calc(100vh - 110px);
  margin: 0 auto;
  position: relative;
}

.container {
  width: 100%;
}

#left-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.eyebrow {
  color: var(--color-accent-dark);
  font-size: .72rem;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: .55rem;
  margin-bottom: 1.5rem;
}

.eyebrow-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-accent-dark);
  box-shadow: 0 0 0 5px rgba(202, 255, 72, .16);
}

.title {
  color: var(--color-ink);
  font-family: Georgia, 'Times New Roman', serif;
  font-size: clamp(3.4rem, 6.8vw, 6.8rem);
  font-weight: 400;
  line-height: .92;
  letter-spacing: -.06em;
  margin-bottom: 1.7rem;
}

.title em {
  color: var(--color-violet);
  font-style: italic;
}

.intro {
  color: var(--color-ink-muted);
  font-size: 1rem;
  line-height: 1.65;
  max-width: 440px;
  margin-bottom: 2rem;
}

.suggestions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: .55rem;
  margin-top: 1.3rem;
  color: var(--color-ink-muted);
  font-size: .78rem;
}

.suggestions button {
  border: 1px solid rgba(24, 24, 24, .16);
  border-radius: 999px;
  background: transparent;
  color: var(--color-ink);
  cursor: pointer;
  padding: .55rem .8rem;
  font: inherit;
  transition: background .2s ease, border-color .2s ease, transform .2s ease;
}

.suggestions button:hover {
  background: var(--color-accent);
  border-color: var(--color-accent);
  transform: translateY(-2px);
}

.visual-panel {
  min-height: 455px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: var(--color-ink);
  border-radius: 3px;
  box-shadow: 18px 22px 0 var(--color-accent);
}

.visual-panel::before {
  content: '';
  position: absolute;
  inset: 17px;
  border: 1px solid rgba(255, 255, 255, .22);
}

.visual-panel img {
  width: min(58%, 250px);
  filter: drop-shadow(0 18px 26px rgba(202, 255, 72, .2));
  animation: float 6s ease-in-out infinite;
}

.visual-panel__label,
.visual-panel__caption,
.visual-panel__stamp {
  position: absolute;
  z-index: 1;
  color: white;
}

.visual-panel__label {
  top: 32px;
  left: 32px;
  font-size: .7rem;
  letter-spacing: .14em;
  text-transform: uppercase;
}

.visual-panel__caption {
  bottom: 29px;
  left: 32px;
  display: grid;
  gap: .3rem;
}

.visual-panel__caption strong { font-size: 1.1rem; }
.visual-panel__caption span { color: rgba(255, 255, 255, .58); font-size: .78rem; }

.visual-panel__stamp {
  right: 32px;
  bottom: 28px;
  color: var(--color-accent);
  font-size: .65rem;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: .12em;
  text-align: right;
}

#conversation-container {
  opacity: 0;
  pointer-events: none;
  transform: translateY(22px);
  transition: opacity .5s ease, transform .5s ease;
}

#conversation-container.show-conversation {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(-3deg); }
  50% { transform: translateY(-14px) rotate(3deg); }
}

@media (max-width: 760px) {
  .workspace { width: min(100% - 36px, 560px); }
  #welcome-wrap { grid-template-columns: 1fr; gap: 3.5rem; padding: 2.5rem 0 5rem; }
  .visual-panel { min-height: 330px; box-shadow: 10px 12px 0 var(--color-accent); }
  .title { font-size: clamp(3.3rem, 17vw, 5.5rem); }
}


/* #conversation-container {
  opacity: 0;
  transition: all 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

#conversation-container.show-conversation {
  opacity: 1;
} */
</style>
