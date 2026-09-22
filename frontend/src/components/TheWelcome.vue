<script setup lang="ts">
import ConversationContainer from './ConversationContainer.vue'
import Header from "@/components/Header.component.vue"
import Help from './HelpCenter.vue'

import { useGlobalVarStore } from "@/stores/globabVar.store"
import { storeToRefs } from "pinia"
import InputSearchComponent from './InputSearch.component.vue'

const globalVarStore = useGlobalVarStore()
const { showConversation } = storeToRefs(globalVarStore)

</script>

<template>
  <div class="window">
    <Header />
    <InputSearchComponent />

    <ConversationContainer
      class="conversation-container"
      :class="{ 'show-conversation': showConversation }"
    />

    <Help />
  </div>
</template>

<style lang="css" scoped>
.conversation-container {
  opacity: 0;
  transition: all 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.conversation-container.show-conversation {
  opacity: 1;
}
</style>
