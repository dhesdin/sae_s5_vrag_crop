<template>
  <div class="conversation-container">
    <MessageBubble v-for="message in messages" :key="message.sender" :sender="message.sender" :content="message.content" />
  </div>
</template>

<script lang="ts" setup>
import MessageBubble from './MessageBubble.vue'

const messages = [
  { sender: "1", content: "Hello, how can I help you today?" },
  { sender: "2", content: "I need help with my account." },
]

</script>

<style lang="css" scoped>
.conversation-container {
  z-index: -1;
  width: 65%;
  height: 80%;
  position: absolute;
}


</style>
