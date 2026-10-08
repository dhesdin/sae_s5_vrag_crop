<template>
  <div class="conversation-overlay" @click.self="closeConversation">
    <section class="conversation-container" role="dialog" aria-modal="true" aria-labelledby="conversation-title">
      <header class="conversation-header">
        <div class="conversation-heading">
          <img src="@/assets/icon.svg" alt="" />
          <div>
            <h2 id="conversation-title">Recherche d’images</h2>
            <p>Affinez votre recherche avec une description</p>
          </div>
        </div>
        <button class="close-button" type="button" aria-label="Fermer les résultats" @click="closeConversation">
          <span aria-hidden="true">&times;</span>
        </button>
      </header>
      <div class="conversation-messages" aria-live="polite">
        <MessageBubble v-for="m in messages" :key="m.id" :response="m" />
      </div>
      <form class="conversation-form" @submit="submitMessage">
        <div class="conversation-field">
        <input
          id="input-message-search"
          class="conversation-input"
          type="text"
          v-model="messageQuery"
          placeholder="Décrivez votre recherche..."
        />
          <button class="conversation-button" type="submit" aria-label="Lancer la recherche">
            <span>Rechercher</span><i class="bi bi-arrow-up-right" aria-hidden="true"></i>
          </button>
        </div>
      </form>
    </section>
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
.conversation-overlay {
  position: fixed;
  z-index: 10;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  box-sizing: border-box;
  background: rgba(24, 24, 24, .38);
  backdrop-filter: blur(5px);
}

.conversation-container {
  position: relative;
  display: flex;
  flex-direction: column;
  width: min(760px, 100%);
  height: min(720px, 86vh);
  min-height: 320px;
  box-sizing: border-box;
  overflow: hidden;
  background: var(--color-paper);
  border: 1px solid rgba(24, 24, 24, .12);
  border-radius: 18px;
  box-shadow: 0 24px 80px rgba(24, 24, 24, .25);
}

.conversation-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(24, 24, 24, .1);
}

.conversation-heading {
  display: flex;
  align-items: center;
  gap: .85rem;
}

.conversation-heading img {
  width: 42px;
  height: auto;
}

.conversation-heading h2 {
  color: var(--color-ink);
  font-size: 1rem;
  font-weight: 700;
}

.conversation-heading p {
  margin-top: .25rem;
  color: var(--color-ink-muted);
  font-size: .78rem;
}

.conversation-messages {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: .5rem 1.5rem 1.25rem;
}

.close-button {
  flex: 0 0 auto;
  width: 38px;
  height: 38px;
  border: 1px solid rgba(24, 24, 24, .12);
  border-radius: 10px;
  background: rgba(255, 255, 255, .6);
  color: var(--color-ink);
  cursor: pointer;
  font-family: inherit;
  font-size: 1.4rem;
  line-height: 1;
  transition: background .2s ease, color .2s ease;
}

.close-button:hover {
  background: var(--color-ink);
  color: white;
}

.conversation-form {
  display: flex;
  padding: 1rem 1.5rem 1.25rem;
  border-top: 1px solid rgba(24, 24, 24, .1);
  background: rgba(255, 255, 255, .35);
}

.conversation-field {
  position: relative;
  width: 100%;
  height: 54px;
  display: flex;
  align-items: center;
}

.conversation-input {
  width: 100%;
  min-width: 0;
  height: 54px;
  box-sizing: border-box;
  border: 1px solid rgba(24, 24, 24, .18);
  border-radius: 11px;
  background: white;
  box-shadow: 0 8px 24px rgba(24, 24, 24, .06);
  color: var(--color-ink);
  font-family: inherit;
  font-size: .9rem;
  padding: 0 148px 0 16px;
  transition: border-color .2s ease, box-shadow .2s ease;
}

.conversation-input::placeholder { color: rgba(24, 24, 24, .48); }

.conversation-input:focus {
  outline: none;
  border-color: var(--color-violet);
  box-shadow: 0 0 0 3px rgba(113, 56, 214, .12);
}

.conversation-button {
  position: absolute;
  right: 6px;
  height: 42px;
  padding: 0 13px;
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .55rem;
  background: var(--color-ink);
  color: white;
  cursor: pointer;
  font-family: inherit;
  font-size: .8rem;
  font-weight: 700;
  white-space: nowrap;
  transition: background .2s ease, transform .2s ease;
}

.conversation-button i {
  color: var(--color-accent);
  font-size: 1.1rem;
}

.conversation-button:hover {
  background: var(--color-violet);
  transform: translateY(-1px);
}

.close-button:focus-visible,
.conversation-button:focus-visible {
  outline: 3px solid rgba(113, 56, 214, .35);
  outline-offset: 2px;
}

@media (max-width: 560px) {
  .conversation-overlay { padding: 12px; }
  .conversation-container { height: min(760px, 92vh); border-radius: 14px; }
  .conversation-header { padding: 1rem; }
  .conversation-messages { padding: .5rem 1rem 1rem; }
  .conversation-form { padding: .85rem 1rem 1rem; }
  .conversation-heading p { max-width: 220px; }
}
</style>
