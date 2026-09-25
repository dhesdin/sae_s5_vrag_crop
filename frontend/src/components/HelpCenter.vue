<!-- filename: documentation.vue -->

<template>

<a href="https://github.com/dhesdin/sae_s5_vrag_crop" target="_blank">
  <div class="circle">
    <p>?</p>
  </div>
</a>

</template>



<style lang="css">

.circle {
  position: absolute;
  right: 1.5rem;
  bottom: 1.5rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-ink);
  color: var(--color-ink);
  transition: all .5s;
}

.circle:hover {
  border-color: var(--color-violet);
  box-shadow: 0 8px 20px rgba(113, 56, 214, .18);
  transform: translateY(-5px);
  /* box-shadow: white 0px 20px 30px -10px; */
}

</style>
