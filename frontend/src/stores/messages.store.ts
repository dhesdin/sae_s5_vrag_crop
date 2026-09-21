import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChatMessage } from '@/models/ChatMessage'

export const useMessagesStore = defineStore('messages', () => {
  const messages = ref<ChatMessage[]>([])

  const addMessage = (message: ChatMessage) => {
    messages.value.push(message)
  }

  return { messages, addMessage }
})
