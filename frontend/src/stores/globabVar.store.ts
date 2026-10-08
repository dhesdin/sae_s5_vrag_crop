import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useGlobalVarStore = defineStore('globalvar', () => {

  const isSearch = ref<boolean>(false)
  const searchQuery = ref<string>('')
  const showConversation = ref<boolean>(false)


  return { isSearch, searchQuery, showConversation }
})
