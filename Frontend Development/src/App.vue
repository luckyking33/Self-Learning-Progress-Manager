<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
  <RouterView v-slot="{ Component, route }">
    <Transition name="route-shell" mode="out-in">
      <component :is="Component" :key="route.fullPath" />
    </Transition>
  </RouterView>
</template>
