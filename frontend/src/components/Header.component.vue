<script setup lang="ts">

</script>

<template>

  <header>
    <div class="wrap">
      <img id="logo" src="@/assets/icon.svg" />
      <span>Aspect</span>
    </div>
  </header>

</template>

<style lang="css" scoped>

  header {
    display: flex;
    align-items: center;
    width: 100vw;
    padding: 1em;
    
  }

  header .wrap {
    display: flex;
    align-items: center;
    gap: 5%
  }
  header .wrap #logo {
    width: 30%;
  }
  header .wrap span {
    color: #fff;
  }


</style>

