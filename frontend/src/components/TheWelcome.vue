<script setup lang="ts">
import ConversationContainer from './ConversationContainer.vue'
import Help from './HelpCenter.vue'
import { ref } from 'vue'

const isSearch = ref<boolean>(false)
const showConversation = ref<boolean>(false)
const searchQuery = ref<string>('')
import { useMessagesStore } from '../stores/messages.store'

const messagesStore = useMessagesStore()

const sendMessage = (message: string) => {
  messagesStore.addMessage({ id: Date.now(), sender: '2', content: message, time: new Date().toLocaleTimeString() })
}

const handleSearch = (e: Event) => {
  e.preventDefault()

  if (!searchQuery.value.trim()) return

  isSearch.value = true

  setTimeout(() => {
    showConversation.value = true
  }, 500)

  sendMessage(searchQuery.value)

  searchQuery.value = ''
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
          <div class="input" id="back-input"></div>
          <input
            class="input"
            id="input-search"
            type="text"
            v-model="searchQuery"
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
