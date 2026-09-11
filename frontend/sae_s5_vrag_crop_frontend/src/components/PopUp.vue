<script setup lang="ts">

import type { Alert } from '@/models/Alert.ts';

defineProps<{
  response: Alert
}>()

</script>

<template>
  <div class="popup">
    {{ response.title }}
    {{ response.content }}
  </div>
</template>

<style scoped lang="css">

template {
  position: absolute;
  background: red;
}

</style>
