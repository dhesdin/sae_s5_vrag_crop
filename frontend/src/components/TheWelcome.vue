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
        <div class="hero-brand" aria-label="Aspect, V-CROP RAG">
          <img src="@/assets/icon.svg" alt="" />
          <span>ASPECT <span class="hero-brand__divider">/</span> V-CROP RAG</span>
        </div>
        <h1 id="page-title" class="title">Retrouvez une image</h1>
        <p class="intro">Décrivez simplement ce que vous cherchez.</p>
        <InputSearchComponent id="input-search-container" />
        <p class="credits">Un projet de Dhesdin Valentin, Gobfert Frédéric et Levitre Mathys</p>
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
  min-height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding-bottom: 3rem;
}

.hero-brand {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: .85rem;
  margin-bottom: 2rem;
  color: var(--color-ink-muted);
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: .16em;
}

.hero-brand img {
  width: 78px;
  height: auto;
}

.hero-brand__divider {
  color: var(--color-violet);
  padding: 0 .2rem;
}

.workspace {
  width: min(760px, calc(100% - 48px));
  margin: 0 auto;
  position: relative;
}

.title {
  color: var(--color-ink);
  font-size: clamp(2rem, 5vw, 3.25rem);
  font-weight: 700;
  letter-spacing: -.045em;
  line-height: 1.1;
}

.intro {
  color: var(--color-ink-muted);
  font-size: 1rem;
  margin: .75rem 0 2rem;
}

.credits {
  margin-top: 2rem;
  color: var(--color-ink-muted);
  font-size: .75rem;
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

@media (max-width: 760px) {
  .workspace { width: calc(100% - 36px); }
  #welcome-wrap { min-height: calc(100vh - 100px); }
}
</style>
