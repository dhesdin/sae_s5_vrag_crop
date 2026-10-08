import { useGlobalVarStore } from "@/stores/globabVar.store"
import { storeToRefs } from "pinia"

import { sendMessage } from "@/scripts/messages"

export function handleSearch(e: Event): void {
  e.preventDefault()

  const globalVarStore = useGlobalVarStore()
  const { isSearch, searchQuery, showConversation } = storeToRefs(globalVarStore)

  if (!searchQuery.value.trim()) return

  isSearch.value = true
  showConversation.value = true

  sendMessage(searchQuery.value)

  searchQuery.value = ''
}


