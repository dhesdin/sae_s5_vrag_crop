<template>

  <header>
    <div class="wrap">
      <img id="logo" src="@/assets/icon.svg" alt="" />
      <span class="brand">Aspect<span class="brand-mark"></span></span>
    </div>
  </header>

</template>

<style lang="css" scoped>

  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: min(1180px, calc(100% - 64px));
    margin: 0 auto;
    padding: 1.8rem 0;

  }

  header .wrap {
    display: flex;
    align-items: center;
    gap: .7rem;
  }
  header .wrap #logo {
    width: 34px;
    height: 23px;
  }
  .brand {
    color: var(--color-ink);
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -.04em;
  }
  .brand-mark { color: var(--color-violet); }
  .header-meta {
    align-items: center;
    color: var(--color-ink-muted);
    display: flex;
    font-size: .7rem;
    gap: .55rem;
    letter-spacing: .08em;
    text-transform: uppercase;
  }
  .status-dot {
    background: var(--color-accent);
    border-radius: 50%;
    height: 7px;
    width: 7px;
  }
  .header-divider { background: rgba(24, 24, 24, .2); height: 14px; width: 1px; }
  @media (max-width: 560px) {
    header { width: calc(100% - 36px); }
    .header-meta { font-size: 0; }
  }


</style>

