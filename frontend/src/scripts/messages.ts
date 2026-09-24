
import { useMessagesStore } from '../stores/messages.store'

export function sendMessage(message: string) {
  const messagesStore = useMessagesStore()

  messagesStore.addMessage({ id: Date.now(), sender: '2', content: message, time: new Date().toLocaleTimeString() })
}
