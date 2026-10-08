
<script lang="ts" setup>

import { handleSearch } from '@/scripts/script'
import { storeToRefs } from 'pinia'
import { useGlobalVarStore } from '../stores/globabVar.store'

const globalVarStore = useGlobalVarStore()
const { isSearch, searchQuery } = storeToRefs(globalVarStore)

</script>

<template>
   <form @submit="handleSearch" class="search-form" id="input-search-form">
      <div class="search-field" :class="{ 'slide-down': isSearch }">
        <input
          class="search-input"
          id="input-search"
          type="text"
          v-model="searchQuery"
          placeholder="Décrivez votre recherche..."
        />
        <button class="search-button" type="submit" aria-label="Lancer la recherche">
          <span>Rechercher</span><i class="bi bi-arrow-up-right" aria-hidden="true"></i>
        </button>
      </div>
    </form>
</template>

<style lang="css">
.search-form {
  display: flex;
  width: 100%;
  justify-content: center;
}

.search-field {
  position: relative;
  width: 100%;
  max-width: 640px;
  height: 60px;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  height: 60px;
  min-width: 0;
  border: 1px solid rgba(24, 24, 24, .18);
  border-radius: 12px;
  background: #fff;
  color: var(--color-ink);
  font-family: inherit;
  font-size: .95rem;
  font-weight: 400;
  padding: 0 150px 0 20px;
  box-sizing: border-box;
  box-shadow: 0 8px 24px rgba(24, 24, 24, .06);
  transition: border-color .2s ease, box-shadow .2s ease;
}

.search-input::placeholder { color: rgba(24, 24, 24, .48); }

.search-input:focus {
  outline: none;
  border-color: var(--color-violet);
  box-shadow: 0 0 0 3px rgba(113, 56, 214, .12), 0 8px 24px rgba(24, 24, 24, .06);
}

.search-button {
  position: absolute;
  right: 8px;
  height: 44px;
  padding: 0 16px;
  border: none;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .65rem;
  background: var(--color-ink);
  color: white;
  cursor: pointer;
  font-family: inherit;
  font-size: .82rem;
  font-weight: 700;
  line-height: 1;
  white-space: nowrap;
  transition: background .2s ease, transform .2s ease;
}

.search-button i {
  color: var(--color-accent);
  font-size: 1.1rem;
}

.search-button:hover {
  background: var(--color-violet);
  transform: translateY(-1px);
}

.search-button:focus-visible {
  outline: 3px solid rgba(113, 56, 214, .35);
  outline-offset: 2px;
}

#back-input {
  display: none;
}

@media (max-width: 480px) {
  .search-input { padding-left: 14px; padding-right: 126px; }
  .search-button { padding: 0 11px; gap: .4rem; }
}
</style>
