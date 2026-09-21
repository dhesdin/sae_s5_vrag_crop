<template>
  <div class="message-container" :class="{ IA: sender == '1' }">
    <p class="content">{{ content }}</p>
    <div class="speech-bubble-tail"></div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  sender: string
  content: string
}>()
</script>

<style scoped>
.message-container {
  margin-top: 2em;
  position: relative;
  width: 50%;
  height: auto;
  border-radius: 10px 10px 0 10px;
  padding: 1em;
  background: green;
  box-sizing: border-box;
  margin-left: auto;
  margin-right: 0;
}

.content {
  font-weight: lighter;
  font-size: 15px;
  margin: 0;
  overflow-wrap: break-word;
}

.speech-bubble-tail {
  position: absolute;
  bottom: -10px;
  right: 0px;
  width: 0;
  height: 0;
  border-top: 15px solid green;
  border-left: 15px solid transparent;
}

.message-container.IA {
  background: purple;
  border-radius: 10px 10px 10px 0;
  margin-left: 0;
  margin-right: auto;
}

.message-container.IA .speech-bubble-tail {
  right: auto;
  left: 0px;
  border-left: none;
  border-right: 15px solid transparent;
  border-top-color: purple;
}
</style>
