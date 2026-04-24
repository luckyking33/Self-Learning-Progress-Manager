<script setup lang="ts">
import { computed, ref } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";

import AppIcon from "@/components/icons/AppIcon.vue";
import { useUserStore } from "@/stores/user";

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");

const redirectTarget = computed(() => {
  const value = route.query.redirect;
  return typeof value === "string" && value.length > 0 ? value : "/learning";
});

const canSubmit = computed(() => {
  return (
    username.value.trim().length >= 3 &&
    email.value.includes("@") &&
    password.value.length >= 5 &&
    password.value === confirmPassword.value
  );
});

async function submit() {
  if (!canSubmit.value) {
    errorMessage.value = "请检查用户名、邮箱和两次输入的密码。";
    return;
  }

  errorMessage.value = "";
  try {
    await userStore.register({
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
    });
    await router.replace(redirectTarget.value);
  } catch (error) {
    errorMessage.value = (error as Error).message;
  }
}
</script>

<template>
  <main class="flex min-h-screen items-center justify-center bg-[linear-gradient(180deg,#f8fafc_0%,#eef2ff_100%)] px-4 py-10">
    <div class="w-full max-w-[980px] overflow-hidden rounded-[36px] bg-white shadow-[0_28px_90px_rgba(15,23,42,0.12)]">
      <div class="grid min-h-[720px] lg:grid-cols-[0.95fr_1.05fr]">
        <section class="flex items-center px-6 py-10 sm:px-10">
          <div class="mx-auto w-full max-w-md">
            <div class="flex items-center gap-3">
              <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-950 text-white">
                <AppIcon name="course" class="h-4 w-4" />
              </div>
              <div>
                <p class="text-[11px] uppercase tracking-[0.32em] text-slate-400">STAR</p>
                <p class="mt-1 text-base font-semibold text-slate-950">创建你的学习身份</p>
              </div>
            </div>

            <div class="mt-10">
              <p class="text-sm uppercase tracking-[0.24em] text-slate-400">Register</p>
              <h1 class="mt-3 text-4xl font-semibold tracking-tight text-slate-950">注册</h1>
              <p class="mt-4 text-sm leading-7 text-slate-500">
                创建账号后我们会自动登录，并把你带到“我的学习”开始使用。
              </p>
            </div>

            <form class="mt-8 space-y-4" @submit.prevent="submit">
              <label class="block">
                <span class="text-sm font-medium text-slate-700">用户名</span>
                <input
                  v-model="username"
                  type="text"
                  autocomplete="username"
                  placeholder="至少 3 位"
                  class="mt-2 w-full rounded-[22px] border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition-all duration-300 focus:border-slate-300 focus:bg-white focus:shadow-[0_16px_32px_rgba(15,23,42,0.06)]"
                />
              </label>

              <label class="block">
                <span class="text-sm font-medium text-slate-700">邮箱</span>
                <input
                  v-model="email"
                  type="email"
                  autocomplete="email"
                  placeholder="you@example.com"
                  class="mt-2 w-full rounded-[22px] border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition-all duration-300 focus:border-slate-300 focus:bg-white focus:shadow-[0_16px_32px_rgba(15,23,42,0.06)]"
                />
              </label>

              <label class="block">
                <span class="text-sm font-medium text-slate-700">密码</span>
                <input
                  v-model="password"
                  type="password"
                  autocomplete="new-password"
                  placeholder="至少 5 位"
                  class="mt-2 w-full rounded-[22px] border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition-all duration-300 focus:border-slate-300 focus:bg-white focus:shadow-[0_16px_32px_rgba(15,23,42,0.06)]"
                />
              </label>

              <label class="block">
                <span class="text-sm font-medium text-slate-700">确认密码</span>
                <input
                  v-model="confirmPassword"
                  type="password"
                  autocomplete="new-password"
                  placeholder="再次输入密码"
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
                <span>{{ userStore.isLoading ? "正在创建账号..." : "注册并进入我的学习" }}</span>
              </button>
            </form>

            <p class="mt-6 text-sm text-slate-500">
              已经有账号？
              <RouterLink
                :to="{ path: '/login', query: route.query.redirect ? { redirect: route.query.redirect } : {} }"
                class="font-medium text-slate-900 underline underline-offset-4"
              >
                去登录
              </RouterLink>
            </p>
          </div>
        </section>

        <section class="relative hidden overflow-hidden bg-slate-50 px-10 py-10 lg:flex lg:flex-col">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(125,211,252,0.34),transparent_36%),radial-gradient(circle_at_bottom_left,rgba(148,163,184,0.15),transparent_34%)]" />
          <div class="relative">
            <p class="text-sm uppercase tracking-[0.3em] text-slate-400">Start clean</p>
            <h2 class="mt-5 text-5xl font-semibold tracking-tight text-slate-950">
              把课程、分叉、笔记和进度放进同一个工作区。
            </h2>
            <p class="mt-6 max-w-md text-base leading-8 text-slate-500">
              注册后你可以收藏课程、记录知识点进度，并在 STAR 里逐步建立自己的课程仓库与学习笔记系统。
            </p>

            <div class="mt-12 space-y-4">
              <div class="rounded-[28px] bg-white px-6 py-5 shadow-[0_16px_40px_rgba(15,23,42,0.06)]">
                <div class="flex items-center gap-3">
                  <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-900 text-white">
                    <AppIcon name="folder" class="h-4 w-4" />
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-slate-900">课程仓库</p>
                    <p class="mt-1 text-sm text-slate-500">把章节、知识点和资源组织成稳定结构。</p>
                  </div>
                </div>
              </div>
              <div class="rounded-[28px] bg-white px-6 py-5 shadow-[0_16px_40px_rgba(15,23,42,0.06)]">
                <div class="flex items-center gap-3">
                  <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-900 text-white">
                    <AppIcon name="note" class="h-4 w-4" />
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-slate-900">学习笔记</p>
                    <p class="mt-1 text-sm text-slate-500">用 Markdown 记录理解、提纲和复盘。</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </main>
</template>
