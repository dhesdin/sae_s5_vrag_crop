<script setup lang="ts">
import type { ChatMessage } from '@/models/ChatMessage'

defineProps<{
  response: ChatMessage
}>()
</script>

<template>
  <div class="message-container" :class="{ IA: response.sender == '1' }">
    <p class="content">{{ response.content }}</p>
    <span id="date">{{ response.time }}</span>
  </div>
</template>

<style scoped>
* {
  font-family:
    -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Segoe UI', Roboto,
    sans-serif;
}

.message-container {
  margin-top: 1.5rem;
  position: relative;
  width: fit-content;
  max-width: 65%;
  min-width: 120px;
  height: auto;
  border-radius: 20px 20px 4px 20px;
  padding: 14px 18px 24px 18px;

  /* Effet glassmorphism iOS (Bulles utilisateur par défaut : teinte verte) */
  background: rgba(198, 255, 52, 0.08);
  backdrop-filter: blur(25px) saturate(180%);
  -webkit-backdrop-filter: blur(25px) saturate(180%);

  border: 1px solid rgba(198, 255, 52, 0.25);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.25),
    inset 0 0 0 1px rgba(255, 255, 255, 0.05);

  box-sizing: border-box;
  margin-left: auto;
  margin-right: 0;

  animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.content {
  font-weight: 400;
  font-size: 14.5px;
  line-height: 1.45;
  color: #f5f5f7;
  margin: 0;
  overflow-wrap: break-word;
  letter-spacing: -0.1px;
}

#date {
  font-size: 10px;
  position: absolute;
  bottom: 8px;
  right: 16px;
  color: rgba(255, 255, 255, 0.45);
  letter-spacing: 0.2px;
}

/* Bulle de l'IA (Teinte violette signature) */
.message-container.IA {
  background: rgba(126, 59, 237, 0.12);
  border: 1px solid rgba(126, 59, 237, 0.35);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.25),
    inset 0 0 0 1px rgba(255, 255, 255, 0.05),
    0 0 15px rgba(126, 59, 237, 0.1);
  border-radius: 20px 20px 20px 4px;
  margin-left: 0;
  margin-right: auto;
}

.message-container.IA #date {
  right: auto;
  left: 16px;
}

@keyframes slideUpFade {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.97);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
