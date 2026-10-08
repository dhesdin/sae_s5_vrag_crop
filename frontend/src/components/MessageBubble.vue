<template>
  <div class="message-container" :class="{ 'is-assistant': response.sender == '1' }">
    <span class="sender">{{ response.sender == '1' ? 'Aspect' : 'Vous' }}</span>
    <p class="content">{{ response.content }}</p>
    <span class="date">{{ response.time }}</span>
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
  display: flex;
  flex-direction: column;
  gap: .4rem;
  position: relative;
  width: fit-content;
  max-width: min(78%, 520px);
  margin: 1rem 0 1rem auto;
  padding: .85rem 1rem .7rem;
  border: 1px solid rgba(24, 24, 24, .08);
  border-radius: 14px 14px 4px 14px;
  background: var(--color-ink);
  color: white;
  box-sizing: border-box;
  animation: slideUpFade .25s ease-out both;
}

.content {
  font-size: .9rem;
  line-height: 1.5;
  margin: 0;
  overflow-wrap: break-word;
}

.sender {
  color: var(--color-accent);
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: .04em;
}

.date {
  align-self: flex-end;
  color: rgba(255, 255, 255, .62);
  font-size: .65rem;
}

.message-container.is-assistant {
  margin-right: auto;
  margin-left: 0;
  border-color: rgba(113, 56, 214, .14);
  border-radius: 14px 14px 14px 4px;
  background: white;
  color: var(--color-ink);
}

.message-container.is-assistant .sender { color: var(--color-violet); }
.message-container.is-assistant .date { color: var(--color-ink-muted); }

@keyframes slideUpFade {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 560px) {
  .message-container { max-width: 90%; }
}
</style>
