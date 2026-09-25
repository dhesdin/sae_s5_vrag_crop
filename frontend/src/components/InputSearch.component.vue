
<script lang="ts" setup>

import { handleSearch } from '@/scripts/script'
import { storeToRefs } from 'pinia'
import { useGlobalVarStore } from '../stores/globabVar.store'

const globalVarStore = useGlobalVarStore()
const { isSearch, searchQuery } = storeToRefs(globalVarStore)

</script>

<template>
   <form @submit="handleSearch" id="input-search-form">
      <div id="input-wrap" :class="{ 'slide-down': isSearch }">
        <input
          id="input-search"
          type="text"
          v-model="searchQuery"
          placeholder="Décrivez votre recherche..."
        />
        <button type="submit" aria-label="Lancer la recherche"><span>Rechercher</span><i class="bi bi-arrow-up-right"></i></button>
      </div>
    </form>
</template>

<style lang="css">

/* Barre de recherche */
form {
  display: flex;
  transition: all 1s cubic-bezier(.77, 0, .175, 1)
}

#input-search-form {
  width: 100%;
}

#input-wrap {
  position: relative;
  width: 100%;
  max-width: 620px;
  height: 64px;
  display: flex;
  align-items: center;
  transition: transform 1s cubic-bezier(.77, 0, .175, 1);
}

#input-search {
  width: 100%;
  height: 64px;
  border: 1px solid rgba(24, 24, 24, .22);
  border-radius: 3px;
  background: rgba(255, 255, 255, .52);
  box-shadow: 0 14px 35px rgba(24, 24, 24, .08);
  color: var(--color-ink);
  font: inherit;
  padding: 0 145px 0 22px;
  transition: border-color .2s ease, box-shadow .2s ease;
}

#input-search::placeholder { color: rgba(24, 24, 24, .48); }
#input-search:focus {
  outline: none;
  border-color: var(--color-violet);
  box-shadow: 0 14px 35px rgba(113, 56, 214, .12);
}

form button[type="submit"] {
  position: absolute;
  right: 8px;
  height: 48px;
  padding: 0 14px;
  border: none;
  border-radius: 2px;
  display: flex;
  align-items: center;
  gap: .7rem;
  background: var(--color-ink);
  color: white;
  cursor: pointer;
  font: inherit;
  font-size: .78rem;
  font-weight: 700;
  transition: background .2s ease, transform .2s ease;
  z-index: 3;
}

form button[type="submit"] i {
  color: var(--color-accent);
  font-size: 1.1rem;
}

form button[type="submit"]:hover {
  background: var(--color-violet);
  transform: translateY(-2px);
}

#back-input {
  display: none;
}

</style>
