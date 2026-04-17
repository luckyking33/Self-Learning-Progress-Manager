<script setup lang="ts">
import { computed } from "vue";

import { iconPaths, type AppIconName } from "@/constants/icons";

const props = withDefaults(
  defineProps<{
    name: AppIconName;
    size?: number;
    class?: string;
  }>(),
  {
    size: 20,
    class: "",
  },
);

const paths = computed(() => iconPaths[props.name]);
</script>

<template>
  <svg
    :class="props.class"
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.7"
    aria-hidden="true"
  >
    <path
      v-for="path in paths"
      :key="path"
      :d="path"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </svg>
</template>
