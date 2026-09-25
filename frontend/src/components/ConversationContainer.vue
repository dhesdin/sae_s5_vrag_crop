<template>
  <div class="conversation-container" role="dialog" aria-modal="true" aria-label="Résultats de recherche">
    <button class="close-button" type="button" aria-label="Fermer les résultats" @click="closeConversation">
      <span aria-hidden="true">&times;</span>
    </button>
    <MessageBubble v-for="m in messages" :key="m.id" :response="m" />
  </div>
</template>

<script lang="ts" setup>
import MessageBubble from './MessageBubble.vue'
import { storeToRefs } from 'pinia'
import { useMessagesStore } from '../stores/messages.store'
import { useGlobalVarStore } from '../stores/globabVar.store'

const messagesStore = useMessagesStore()
const { messages } = storeToRefs(messagesStore)
const globalVarStore = useGlobalVarStore()
const { isSearch, showConversation } = storeToRefs(globalVarStore)

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


</style>
