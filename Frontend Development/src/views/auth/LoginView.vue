<script setup lang="ts">
import { computed, ref } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";

import AppIcon from "@/components/icons/AppIcon.vue";
import { useUserStore } from "@/stores/user";

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const identity = ref("");
const password = ref("");
const errorMessage = ref("");

const redirectTarget = computed(() => {
  const value = route.query.redirect;
  return typeof value === "string" && value.length > 0 ? value : "/learning";
});

const canSubmit = computed(() => identity.value.trim().length > 0 && password.value.length >= 5);

async function submit() {
  if (!canSubmit.value) {
    errorMessage.value = "请输入用户名或邮箱，并填写至少 5 位密码。";
    return;
  }

  errorMessage.value = "";
  try {
    await userStore.login(identity.value.trim(), password.value);
    await router.replace(redirectTarget.value);
  } catch (error) {
    errorMessage.value = (error as Error).message;
  }
}
</script>

<template>
  <main class="flex min-h-screen items-center justify-center bg-[linear-gradient(180deg,#f8fafc_0%,#eef2ff_100%)] px-4 py-10">
    <div class="w-full max-w-[980px] overflow-hidden rounded-[36px] bg-white shadow-[0_28px_90px_rgba(15,23,42,0.12)]">
      <div class="grid min-h-[680px] lg:grid-cols-[1.05fr_0.95fr]">
        <section class="relative hidden overflow-hidden bg-slate-950 px-10 py-10 text-white lg:flex lg:flex-col">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(125,211,252,0.28),transparent_34%),radial-gradient(circle_at_bottom_right,rgba(148,163,184,0.2),transparent_38%)]" />
          <div class="relative">
            <div class="flex items-center gap-3">
              <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/10">
                <AppIcon name="sparkles" class="h-5 w-5" />
              </div>
              <div>
                <p class="text-[11px] uppercase tracking-[0.32em] text-white/45">STAR</p>
                <p class="mt-1 text-lg font-semibold">Self-Study Studio</p>
              </div>
            </div>
            <div class="mt-16 max-w-md">
              <p class="text-sm uppercase tracking-[0.3em] text-white/45">Welcome back</p>
              <h1 class="mt-5 text-5xl font-semibold tracking-tight">把学习进度重新接起来。</h1>
              <p class="mt-6 text-base leading-8 text-white/68">
                登录后我们会恢复你的课程、报名状态和上次学习位置，让你从刚刚停下来的地方继续。
              </p>
            </div>
          </div>
        </section>

        <section class="flex items-center px-6 py-10 sm:px-10">
          <div class="mx-auto w-full max-w-md">
            <div class="flex items-center gap-3 lg:hidden">
              <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-950 text-white">
                <AppIcon name="sparkles" class="h-4 w-4" />
              </div>
              <div>
                <p class="text-[11px] uppercase tracking-[0.32em] text-slate-400">STAR</p>
                <p class="mt-1 text-base font-semibold text-slate-950">欢迎回来</p>
              </div>
            </div>

            <div class="mt-10 lg:mt-0">
              <p class="text-sm uppercase tracking-[0.24em] text-slate-400">Sign In</p>
              <h2 class="mt-3 text-4xl font-semibold tracking-tight text-slate-950">登录</h2>
              <p class="mt-4 text-sm leading-7 text-slate-500">
                使用用户名或邮箱登录，继续你的 STAR 学习工作流。
              </p>
            </div>

            <form class="mt-8 space-y-4" @submit.prevent="submit">
              <label class="block">
                <span class="text-sm font-medium text-slate-700">用户名或邮箱</span>
                <input
                  v-model="identity"
                  type="text"
                  autocomplete="username"
                  placeholder="user1 或 user1@example.com"
                  class="mt-2 w-full rounded-[22px] border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition-all duration-300 focus:border-slate-300 focus:bg-white focus:shadow-[0_16px_32px_rgba(15,23,42,0.06)]"
                />
              </label>

              <label class="block">
                <span class="text-sm font-medium text-slate-700">密码</span>
                <input
                  v-model="password"
                  type="password"
                  autocomplete="current-password"
                  placeholder="至少 5 位"
                  class="mt-2 w-full rounded-[22px] border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition-all duration-300 focus:border-slate-300 focus:bg-white focus:shadow-[0_16px_32px_rgba(15,23,42,0.06)]"
                />
              </label>

              <p v-if="errorMessage" class="rounded-2xl bg-rose-50 px-4 py-3 text-sm text-rose-600">
                {{ errorMessage }}
              </p>

              <button
                type="submit"
                :disabled="userStore.isLoading"
                class="inline-flex w-full items-center justify-center gap-2 rounded-full bg-slate-950 px-5 py-3 text-sm font-medium text-white transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_rgba(15,23,42,0.16)] disabled:cursor-not-allowed disabled:opacity-70"
              >
                <AppIcon name="sparkles" class="h-4 w-4" />
                <span>{{ userStore.isLoading ? "正在登录..." : "登录并继续学习" }}</span>
              </button>
            </form>

            <p class="mt-6 text-sm text-slate-500">
              还没有账号？
              <RouterLink
                :to="{ path: '/register', query: route.query.redirect ? { redirect: route.query.redirect } : {} }"
                class="font-medium text-slate-900 underline underline-offset-4"
              >
                去注册
              </RouterLink>
            </p>
          </div>
        </section>
      </div>
    </div>
  </main>
</template>
