
<script lang="ts" setup>

import { handleSearch } from '@/scripts/script'
import { storeToRefs } from 'pinia'
import { useGlobalVarStore } from '../stores/globabVar.store'

const globalVarStore = useGlobalVarStore()
const { isSearch, searchQuery } = storeToRefs(globalVarStore)

</script>

<template>
   <form @submit="handleSearch">
      <div id="input-wrap" :class="{ 'slide-down': isSearch }">
        <div class="input" id="back-input"></div>
        <input
          class="input"
          id="input-search"
          type="text"
          v-model="searchQuery"
          placeholder="Décrivez votre recherche..."
        />
        <input type="submit" value="Rechercher" />
      </div>
    </form>
</template>

<style lang="css" scoped>


</style>

