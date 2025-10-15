<script>
    let { color, point } = $props();
</script>

<div
    class="mb-2 last:mb-4 rounded-lg border border-{color}-200/50 bg-{color}-50/50 p-3 dark:border-{color}-900/30 dark:bg-{color}-950/20"
>
    <span class="text-foreground/90 text-sm">{point}</span>
</div>
