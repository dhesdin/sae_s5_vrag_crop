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
  <div class="window">
    <Header />

    <div id="welcome-wrap">
      <div id="left-container" class="container">
        <p class="title">Bienvenue sur <span>Aspect</span></p>
        <InputSearchComponent id="input-search-container" />
      </div>

      <div id="right-container" class="container">
        <img src="../assets/icon.svg" alt="Icon" />
      </div>
    </div>
    <!-- <ConversationContainer
      id="conversation-container"
      :class="{ 'show-conversation': showConversation }"
    /> -->

    <Help />
  </div>
</template>

<style lang="css" scoped>

#welcome-wrap {
  display: flex;
  align-items: center;
  justify-content: center;  /* centre horizontalement les 2 containers */
  gap: 2rem;                 /* espace entre les deux containers, ajuste selon besoin */
  max-width: 1200px;         /* limite la largeur totale, ajuste selon ton design */
  margin: 0 auto;            /* centre le wrap lui-même dans la page */
}

.container {
  width: 40%;
}

#left-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;   /* aligne tous les enfants (titre, input) à gauche */
  text-align: left;
}

.title {
  font-size: 5rem;
}


/* #conversation-container {
  opacity: 0;
  transition: all 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

#conversation-container.show-conversation {
  opacity: 1;
} */
</style>
