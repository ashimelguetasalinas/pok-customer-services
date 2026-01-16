<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 transition-colors">
    <header
      class="flex items-center justify-between px-6 py-4
             border-b border-gray-200 dark:border-gray-700"
    >
      <h1 class="font-bold text-gray-900 dark:text-gray-100">
        POK Customer Services
      </h1>

      <ThemeToggle />
    </header>

    <main>
      <slot />
    </main>
  </div>
</template>
