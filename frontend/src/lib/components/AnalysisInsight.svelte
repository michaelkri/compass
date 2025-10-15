<script>
    let { title, category, requirement, candidate_fact, summary } = $props();
</script>

<div class="p-4 border-border border-1 mb-4 rounded-lg">
    <div class="flex justify-between mb-4">
        <h4 class="font-semibold">{title}</h4>
        <span class="border-border rounded-md border px-2 py-0.5 text-xs">{category}</span>
    </div>

    <div class="font-medium mb-1 mt-2">Required:</div>
    <div class="border-l-2 border-gray-500 px-2 py-0.5 italic">"{requirement}"</div>
    {#if candidate_fact !== null}
        <div class="font-medium mb-1 mt-2">Actual:</div>
        <div class="border-l-2 border-gray-500 px-2 py-0.5 italic">"{candidate_fact}"</div>
    {/if}
    <p class="mt-2">{summary}</p>
</div>