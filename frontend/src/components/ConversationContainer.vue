<template>
  <div class="conversation-container" role="dialog" aria-modal="true" aria-label="Résultats de recherche">
    <button class="close-button" type="button" aria-label="Fermer les résultats" @click="closeConversation">
      <span aria-hidden="true">&times;</span>
    </button>
    <MessageBubble v-for="m in messages" :key="m.id" :response="m" />
    <form id="input-message-form" @submit="submitMessage">
      <div id="input-wrap" :class="{ 'slide-down': isSearch }">
        <input
          id="input-message-search"
          type="text"
          v-model="messageQuery"
          placeholder="Décrivez votre recherche..."
        />
        <button type="submit" aria-label="Lancer la recherche"><span>Rechercher</span><i class="bi bi-arrow-up-right"></i></button>
      </div>
    </form>
  </div>
</template>

<script lang="ts" setup>
import MessageBubble from './MessageBubble.vue'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'
import { useMessagesStore } from '../stores/messages.store'
import { useGlobalVarStore } from '../stores/globabVar.store'
import { handleSearch } from '@/scripts/script'

const messagesStore = useMessagesStore()
const { messages } = storeToRefs(messagesStore)
const globalVarStore = useGlobalVarStore()
const { isSearch, searchQuery, showConversation } = storeToRefs(globalVarStore)
const messageQuery = ref('')

function submitMessage(event: Event) {
  searchQuery.value = messageQuery.value
  handleSearch(event)
  messageQuery.value = ''
}

function closeConversation() {
  showConversation.value = false
  isSearch.value = false
}

</script>

<style lang="css" scoped>
.conversation-container {
  position: fixed;
  z-index: 10;
  inset: 0;
  width: min(760px, calc(100vw - 40px));
  height: min(80vh, 640px);
  margin: auto;
  padding: 3.5rem 2rem 2rem;
  box-sizing: border-box;
  overflow-y: auto;
  overflow-x: hidden;
  background: var(--color-paper);
  border: 1px solid rgba(24, 24, 24, .18);
  border-radius: 4px;
  box-shadow: 0 24px 80px rgba(24, 24, 24, .28), 12px 12px 0 var(--color-accent);
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 36px;
  height: 36px;
  border: 1px solid rgba(24, 24, 24, .2);
  border-radius: 50%;
  background: transparent;
  color: var(--color-ink);
  cursor: pointer;
  font-size: 1.5rem;
  line-height: 1;
  transition: background .2s ease, color .2s ease, transform .2s ease;
}

.close-button:hover {
  background: var(--color-ink);
  color: var(--color-accent);
  transform: rotate(90deg);
}


#input-message-form {
  position: absolute;
  right: 2rem;
  bottom: 1.5rem;
  left: 2rem;
  display: flex;
  justify-content: center;
}

#input-wrap {
  position: relative;
  width: 100%;
  max-width: 620px;
  height: 64px;
  display: flex;
  align-items: center;
}

#input-message-search {
  width: 100%;
  height: 64px;
  border: 1px solid rgba(24, 24, 24, .22);
  border-radius: 3px;
  background: rgba(255, 255, 255, .52);
  box-shadow: 0 14px 35px rgba(24, 24, 24, .08);
  color: var(--color-ink);
  font: inherit;
  padding: 0 145px 0 22px;
  transition: border-color .2s ease, box-shadow .2s ease;
}

#input-message-search::placeholder { color: rgba(24, 24, 24, .48); }

#input-message-search:focus {
  outline: none;
  border-color: var(--color-violet);
  box-shadow: 0 14px 35px rgba(113, 56, 214, .12);
}

#input-message-form button[type="submit"] {
  position: absolute;
  right: 8px;
  height: 48px;
  padding: 0 14px;
  border: none;
  border-radius: 2px;
  display: flex;
  align-items: center;
  gap: .7rem;
  background: var(--color-ink);
  color: white;
  cursor: pointer;
  font: inherit;
  font-size: .78rem;
  font-weight: 700;
  transition: background .2s ease, transform .2s ease;
  z-index: 3;
}

#input-message-form button[type="submit"] i {
  color: var(--color-accent);
  font-size: 1.1rem;
}

#input-message-form button[type="submit"]:hover {
  background: var(--color-violet);
  transform: translateY(-2px);
}

</style>
