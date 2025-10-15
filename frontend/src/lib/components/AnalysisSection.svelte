<script>
    let { children, title } = $props();

    let isCollapsed = $state(true);
</script>

<div class="border-border bg-background/50 mb-3 rounded-lg border px-4">
    <div class="flex">
        <button
            type="button"
            class="flex flex-1 items-center justify-between rounded-md py-4 font-semibold cursor-pointer"
            onclick={() => (isCollapsed = !isCollapsed)}
        >
            <div class="flex items-center space-x-2">
                <!-- <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="lucide lucide-circle-check mt-0.5 h-4 w-4 shrink-0 text-{color}-600 dark:text-{color}-400"
                    aria-hidden="true"
                >
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="m9 12 2 2 4-4"></path>
                </svg> -->
                <h3>{title}</h3>
            </div>
            {#if isCollapsed}
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="lucide lucide-chevron-down size-4"
                    ><path d="m6 9 6 6 6-6"></path>
                </svg>
            {:else}
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="lucide lucide-chevron-up size-4"
                    ><path d="m18 15-6-6-6 6"></path>
                </svg>
            {/if}
        </button>
    </div>

    <div role="region" class="overflow-hidden text-sm">
        {#if !isCollapsed}
            {@render children?.()}
            <!-- {#each points as point}
                <div
                    class="mb-2 last:mb-4 rounded-lg border border-{color}-200/50 bg-{color}-50/50 p-3 dark:border-{color}-900/30 dark:bg-{color}-950/20"
                >
                    <span class="text-foreground/90 text-sm">{point}</span>
                </div>
            {/each} -->
        {/if}
    </div>
</div>
