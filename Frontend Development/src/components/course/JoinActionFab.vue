<script setup lang="ts">
import type { JoinState } from "@/types/course";

defineProps<{
  joinState: JoinState;
  isEnrolled: boolean;
}>();

const emit = defineEmits<{
  (event: "join"): void;
}>();
</script>

<template>
  <button
    :class="[
      'fixed bottom-7 right-7 z-20 inline-flex items-center gap-3 rounded-full px-6 py-4 text-sm font-medium text-white shadow-[0_20px_45px_rgba(15,23,42,0.18)] transition-all duration-300 ease-in-out',
      joinState === 'success'
        ? 'bg-emerald-500 hover:bg-emerald-500'
        : 'bg-slate-900 hover:-translate-y-1 hover:shadow-[0_24px_48px_rgba(15,23,42,0.24)]',
    ]"
    @click="emit('join')"
  >
    <span
      :class="[
        'flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-base transition-all duration-300',
        joinState === 'loading' ? 'animate-spin' : '',
      ]"
    >
      {{ joinState === "loading" ? "●" : joinState === "success" ? "✓" : "✦" }}
    </span>
    <span>
      {{
        joinState === "loading"
          ? "正在加入学习..."
          : joinState === "success"
            ? "加入成功"
            : isEnrolled
              ? "继续学习"
              : "加入学习"
      }}
    </span>
  </button>
</template>
