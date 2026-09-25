<template>
  <div class="message-container" :class="{ IA: response.sender == '1' }">
    <p class="content">{{ response.content }}</p>
    <span id="date">{{ response.time }}</span>
  </div>
</template>

<script setup lang="ts">
import type { ChatMessage } from '@/models/ChatMessage';

defineProps<{
  response: ChatMessage
}>()
</script>

<style scoped>
.message-container {
  margin-top: 2em;
  position: relative;
  width: 50%;
  height: auto;
  padding: 1em;

  background: rgba(202, 255, 72, 0.1);


  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5.5px);
  -webkit-backdrop-filter: blur(5.5px);
  border: 1px solid rgba(24, 24, 24, .18);
  box-sizing: border-box;
  margin-left: auto;
  margin-right: 0;


  animation: slideUpFade .7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.content {
  font-weight: lighter;
  font-size: 15px;
  margin: 0;
  overflow-wrap: break-word;
}

#date {
  font-size: 10px;
  position: absolute;
  bottom: 0;
  color: grey
}

.message-container.IA {
  background: rgba(113, 56, 214, 0.1);

  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5.5px);
  -webkit-backdrop-filter: blur(5.5px);
  border: 1px solid rgba(24, 24, 24, .18);
  box-sizing: border-box;
  margin-left: auto;
  margin-right: 0;
  border-radius: 16px 16px 16px 0;
  margin-left: 0;
  margin-right: auto;
}






@keyframes slideUpFade {
  0% {
    opacity: 0;
    transform: translateY(20px); /* Commence 20px plus bas */
  }
  100% {
    opacity: 1;
    transform: translateY(0); /* Remonte à sa position initiale */
  }
}
</style>
