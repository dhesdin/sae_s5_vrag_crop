
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

<style lang="css">

/* Barre de recherche */
form {
  display: flex;
  transition: all 1s cubic-bezier(.77, 0, .175, 1)
}

form:has(#input-wrap.slide-down) {
  transform: translateY(20vh);
}


#input-search-form {
  width: 100%;
}

#input-wrap {
  position: relative;
  width: 620px; /* Ajusté à la taille du fond pour centrer proprement */
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 1s cubic-bezier(.77, 0, .175, 1);
}

input {
  max-width: 580px;
  width: 490px;
  height: 50px;
  border-radius: 10px;
  padding: 0 110px 0 20px; /* Espace à droite pour ne pas écrire sous le bouton */
  /* From https://css.glass */
  color: white;
/* From https://css.glass */
/* From https://css.glass */
background: rgba(0, 0, 0, 1);
border-radius: 16px;
box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
backdrop-filter: blur(6.7px);
-webkit-backdrop-filter: blur(6.7px);
border: 1px solid rgba(0, 0, 0, 1);
}

input:focus {
  outline: none;
}

.input {
  position: absolute;
}

/* Bouton positionné à l'intérieur de l'input */
form input[type="submit"] {
  position: absolute;
  right: 5px; /* Décale le bouton vers l'intérieur à droite */
  width: auto;
  height: 40px;
  padding: 0 15px;
  border-radius: 8px;
  border: none;

  color: white;
  cursor: pointer;
  transition: background 0.3s;
  z-index: 3; /* S'assure qu'il est cliquable au-dessus de l'input */
}

form input[type="submit"]:hover {
  background: #6a11cb;
}

#back-input {
  width: 620px;
  height: 50px;
  background: linear-gradient(to right, #C6FF34, #C6FF34, #7E3BED, #7E3BED);
  background-size: 800% 600%;
  filter: blur(20px);
  animation: gradientAnimation 10s ease infinite;
}

</style>
