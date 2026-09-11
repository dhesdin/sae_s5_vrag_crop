<script setup lang="ts">
import type { Alert } from '@/models/Alert.ts';
import { onMounted, onUnmounted } from 'vue';

const props = defineProps<{
  message: Alert
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

let timer: number | null = null

onMounted(() => {
  // Disparaît automatiquement après 3 secondes
  timer = window.setTimeout(() => {
    emit('close')
  }, 3000)
})

onUnmounted(() => {
  if (timer) clearTimeout(timer)
})

const closeAlert = () => {
  if (timer) clearTimeout(timer)
  emit('close')
}
</script>

<template>
  <div id="popup">
    <div class="popup-glow"></div>
    <div class="popup-content">
      <div class="popup-header">
        <div class="header-left">
          <span class="popup-dot"></span>
          <p class="alert-item" id="title">{{ message.title }}</p>
        </div>
        <button class="close-btn" @click="closeAlert" aria-label="Fermer">×</button>
      </div>
      <p class="alert-item" id="text">{{ message.content }}</p>
    </div>
  </div>
</template>

<style scoped lang="css">
* {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif;
}

#popup {
  position: fixed;
  top: 30px;
  right: 30px;
  width: 340px;
  z-index: 1000;
  border-radius: 20px;
  background: rgba(20, 20, 25, 0.65);
  backdrop-filter: blur(25px) saturate(180%);
  -webkit-backdrop-filter: blur(25px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6),
  inset 0 0 0 1px rgba(255, 255, 255, 0.05),
  0 0 25px rgba(126, 59, 237, 0.2);
  overflow: hidden;
  animation: slideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.popup-glow {
  height: 2px;
  width: 100%;
  background: linear-gradient(90deg, #7E3BED, #C6FF34);
  box-shadow: 0 0 10px #C6FF34;
}

.popup-content {
  padding: 20px 22px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.popup-dot {
  width: 7px;
  height: 7px;
  background-color: #C6FF34;
  border-radius: 50%;
  box-shadow: 0 0 10px #C6FF34, 0 0 4px #7E3BED;
}

#title {
  color: #f5f5f7;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  letter-spacing: -0.2px;
}

#text {
  color: rgba(255, 255, 255, 0.65);
  font-size: 13.5px;
  line-height: 1.45;
  margin: 0;
  letter-spacing: -0.1px;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: rgba(255, 255, 255, 0.6);
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-30px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
