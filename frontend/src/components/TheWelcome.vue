<script setup lang="ts">
import { ref } from 'vue'
<<<<<<< HEAD:frontend/src/components/TheWelcome.vue
import { useMessagesStore } from '../stores/messages.store.ts'
=======

import { useMessagesStore } from '../stores/messages.store'
>>>>>>> d6dec40e4734db395aada0b78ba4f9cbfcfb6a6b:frontend/sae_s5_vrag_crop_frontend/src/components/TheWelcome.vue

/* Import des models */
import type { Alert } from '@/models/Alert'
import type { ChatMessage } from '@/models/ChatMessage.ts'

/* Import des components */
import AlertComponent from '@/components/AlertComponent.vue'
import ConversationContainer from '@/components/ConversationContainer.vue'
import Help from '@/components/HelpCenter.vue'

const messagesStore = useMessagesStore()

const isSearch = ref<boolean>(false)
const showConversation = ref<boolean>(false)
const showAlert = ref<boolean>(true)

const searchQuery = ref<string>('')

const sendMessage = (message: string): void => {
  const sendedMessage: ChatMessage = {
    id: Date.now(),
    sender: '2',
    content: message,
    time: new Date().toLocaleTimeString(),
  }
  messagesStore.addMessage(sendedMessage)
}

const handleSearch = (e: Event): void => {
  e.preventDefault()

  if (!searchQuery.value.trim()) return

  isSearch.value = true

  setTimeout(() => {
    showConversation.value = true
  }, 500)

  sendMessage(searchQuery.value)

  searchQuery.value = ''
}

const AlertTest: Alert = {
  title: 'Test',
  content: 'Je suis une alert',
}
</script>

<template>
  <div class="window">
    <div class="welcome-wrap">
      <div class="top-wrap">
        <img class="not-selected" :class="{ 'slide-icon': isSearch }" src="../assets/icon.svg" />
        <p class="not-selected" :class="{ 'hidden-top': isSearch }">
          Bienvenue sur <span>Aspect</span>
        </p>
      </div>

      <form @submit="handleSearch">
        <div id="input-wrap" :class="{ 'slide-down': isSearch }">
          <div id="back-input" class="input"></div>
          <input
            id="input-search"
            v-model="searchQuery"
            class="input"
            type="text"
            placeholder="Décrivez votre recherche..."
          />
          <input type="submit" value="Rechercher" />
        </div>
      </form>
    </div>

    <ConversationContainer
      class="conversation-container"
      :class="{ 'show-conversation': showConversation }"
    />

    <AlertComponent v-if="showAlert" :message="AlertTest" @close="showAlert = false" />
    <Help />
  </div>
</template>

<style lang="css" scoped>
.conversation-container {
  opacity: 0;
  transition: all 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.conversation-container.show-conversation {
  opacity: 1;
}
</style>
