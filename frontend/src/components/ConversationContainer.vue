<template>
  <div class="conversation-container">
    <MessageBubble v-for="m in messages" :key="m.id" :response="m" />
  </div>
</template>

<script lang="ts" setup>
import MessageBubble from './MessageBubble.vue'
import { storeToRefs } from 'pinia'
import { useMessagesStore } from '../stores/messages.store'

const messagesStore = useMessagesStore()
const { messages } = storeToRefs(messagesStore)
// const messages = [
//   { id: 1, sender: "1", content: "Hello, how can I help you?", time: new Date() },
//   { id: 2, sender: "2", content: "I need assistance with my order.", time: new Date() }
// ]



</script>

<style lang="css" scoped>
.conversation-container {
  overflow-y: auto;
  overflow-x: hidden;
  width: min(760px, 100%);
  max-height: 360px;
  margin: 0 auto 4rem;
  padding: 0 1rem 1.5rem;
  box-sizing: border-box;
}


</style>
