<script setup lang="ts">
import { computed, onMounted } from "vue";
import { RouterLink, RouterView, useRoute } from "vue-router";

import AppIcon from "@/components/icons/AppIcon.vue";
import { useUserStore } from "@/stores/user";

type NavItem = {
  name: string;
  to: string;
  label: string;
  iconName: "course" | "folder" | "note" | "settings";
  exact?: boolean;
};

const route = useRoute();
const userStore = useUserStore();

const navItems: NavItem[] = [
  {
    name: "square",
    to: "/square",
    label: "课程广场",
    iconName: "course",
    exact: true,
  },
  {
    name: "learning",
    to: "/learning",
    label: "我的学习",
    iconName: "folder",
    exact: true,
  },
  {
    name: "notes",
    to: "/notes",
    label: "我的笔记",
    iconName: "note",
    exact: true,
  },
  {
    name: "settings",
    to: "/settings",
    label: "个人设置",
    iconName: "settings",
    exact: true,
  },
];

const currentLabel = computed(() => {
  if (route.path.startsWith("/course/")) {
    return "课程详情";
  }

  return navItems.find((item) => route.path === item.to)?.label ?? "STAR";
});

function isActive(item: NavItem) {
  if (item.exact) {
    return route.path === item.to;
  }

  return route.path.startsWith(item.to);
}

onMounted(async () => {
  await userStore.bootstrap();
});
</script>

<template>
  <div class="min-h-screen bg-transparent text-slate-900">
    <aside
      class="fixed inset-x-4 top-4 z-30 rounded-[28px] border border-white/50 bg-white/55 px-4 py-4 shadow-[0_24px_60px_rgba(15,23,42,0.08)] backdrop-blur-2xl lg:inset-y-4 lg:left-4 lg:right-auto lg:w-[260px] lg:px-5"
    >
      <div class="flex items-center gap-3 rounded-[22px] px-2 py-2">
        <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-950 text-white">
          <AppIcon name="sparkles" class="h-5 w-5" />
        </div>
        <div>
          <p class="text-[11px] uppercase tracking-[0.32em] text-slate-400">STAR</p>
          <h1 class="mt-1 text-base font-semibold text-slate-950">Self-Study Studio</h1>
        </div>
      </div>

      <div
        class="mt-5 flex items-center gap-3 rounded-[22px] bg-white/70 px-3 py-3 shadow-[0_14px_30px_rgba(15,23,42,0.05)]"
      >
        <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-900 text-sm font-semibold text-white">
          {{ userStore.currentUser?.avatar ?? "LY" }}
        </div>
        <div class="min-w-0">
          <p class="truncate text-sm font-semibold text-slate-900">
            {{ userStore.currentUser?.name ?? "学习者" }}
          </p>
          <p class="truncate text-xs text-slate-500">
            {{ userStore.currentUser?.headline ?? "正在建立自己的课程仓库" }}
          </p>
        </div>
      </div>

      <div class="mt-6 hidden lg:block">
        <p class="px-3 text-[11px] uppercase tracking-[0.24em] text-slate-400">Workspace</p>
        <nav class="mt-3 space-y-2">
          <RouterLink
            v-for="item in navItems"
            :key="item.name"
            :to="item.to"
            :class="[
              'group flex items-center gap-3 rounded-[22px] px-3 py-3 text-sm font-medium transition-all duration-300 ease-in-out',
              isActive(item)
                ? 'bg-white text-slate-950 shadow-[0_16px_32px_rgba(15,23,42,0.08)]'
                : 'text-slate-500 hover:-translate-y-0.5 hover:bg-white/80 hover:text-slate-900 hover:shadow-[0_14px_28px_rgba(15,23,42,0.06)]',
            ]"
          >
            <span
              :class="[
                'flex h-10 w-10 items-center justify-center rounded-2xl transition-all duration-300',
                isActive(item) ? 'bg-slate-100 text-slate-900' : 'bg-white/70 text-slate-400 group-hover:text-slate-700',
              ]"
            >
              <AppIcon :name="item.iconName" class="h-4 w-4" />
            </span>
            <span>{{ item.label }}</span>
          </RouterLink>
        </nav>
      </div>

      <div class="mt-5 grid grid-cols-2 gap-2 lg:hidden">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :to="item.to"
          :class="[
            'flex items-center justify-center gap-2 rounded-2xl px-3 py-3 text-xs font-medium transition-all duration-300',
            isActive(item)
              ? 'bg-white text-slate-950 shadow-[0_12px_24px_rgba(15,23,42,0.08)]'
              : 'bg-transparent text-slate-500 hover:bg-white/70 hover:text-slate-900',
          ]"
        >
          <AppIcon :name="item.iconName" class="h-4 w-4" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </div>
    </aside>

    <div class="px-4 pb-6 pt-[268px] lg:pl-[296px] lg:pr-6 lg:pt-6">
      <div class="mx-auto max-w-[1480px]">
        <header class="mb-5 flex items-center justify-between gap-4 px-1">
          <div>
            <p class="text-[11px] uppercase tracking-[0.28em] text-slate-400">Current Space</p>
            <h2 class="mt-2 text-2xl font-semibold tracking-tight text-slate-950">{{ currentLabel }}</h2>
          </div>
          <div
            class="hidden items-center gap-2 rounded-full border border-white/70 bg-white/60 px-4 py-2 text-sm text-slate-500 shadow-[0_12px_30px_rgba(15,23,42,0.06)] backdrop-blur-xl md:flex"
          >
            <AppIcon name="sparkles" class="h-4 w-4" />
            <span>STAR self-study workflow</span>
          </div>
        </header>

        <RouterView v-slot="{ Component, route: childRoute }">
          <Transition name="route-page" mode="out-in">
            <component :is="Component" :key="childRoute.fullPath" />
          </Transition>
        </RouterView>
      </div>
    </div>
  </div>
</template>
