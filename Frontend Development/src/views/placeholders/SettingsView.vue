<template>
  <section class="space-y-6">
    <div class="rounded-[32px] bg-white px-7 py-7 shadow-[0_20px_60px_rgba(15,23,42,0.08)]">
      <p class="text-[11px] uppercase tracking-[0.28em] text-slate-400">Settings</p>
      <h1 class="mt-3 text-4xl font-semibold tracking-tight text-slate-950">个人设置</h1>
      <p class="mt-4 max-w-2xl text-sm leading-7 text-slate-500">
        这里会承载账户信息、界面偏好、通知策略和学习隐私选项。
      </p>
    </div>

    <div class="grid gap-5 md:grid-cols-2">
      <article
        v-for="card in ['账户偏好', '通知设置', '隐私与可见性', '界面实验项']"
        :key="card"
        class="rounded-[28px] bg-white px-6 py-6 shadow-[0_18px_45px_rgba(15,23,42,0.08)] transition-all duration-300 ease-in-out hover:-translate-y-1 hover:shadow-[0_22px_55px_rgba(15,23,42,0.1)]"
      >
        <p class="text-xs uppercase tracking-[0.22em] text-slate-400">{{ card }}</p>
        <p class="mt-3 text-sm leading-7 text-slate-500">占位模块，等待真实设置项与保存接口接入。</p>
      </article>
    </div>
  </section>
</template>
