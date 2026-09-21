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
  overflow-x: none;
  z-index: -1;
  width: 80%;
  height: 80%;
  position: absolute;
}


</style>
