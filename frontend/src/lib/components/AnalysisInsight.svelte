<script>
    let { title, category, requirement, candidate_fact, summary } = $props();

    // set color based on category
    let backgroundColor;
    let style;

    switch (category) {
        case "Match":
            backgroundColor = "bg-green-700";
            style = "bg-green-300 text-green-900";
            break;
        case "Missing":
            backgroundColor = "bg-red-700";
            style = "bg-red-300 text-red-900";
            break;
        case "Partial":
            backgroundColor = "bg-amber-700";
            style = "bg-yellow-300 text-yellow-900";
            break;
        case "Quick Learn":
            backgroundColor = "bg-indigo-700";
            style = "bg-indigo-300 text-indigo-900";
            break;
        default:
            backgroundColor = "bg-gray-100";
            style = "bg-gray-300 text-gray-900";
    }
</script>

<!-- <div class="p-4 {backgroundColor} {borderColor} {textColor} border-2 mb-4 rounded-lg">
    <div class="flex justify-between mb-4">
        <h4 class="font-semibold">{title}</h4>
        <span class="border-2 {borderColor} rounded-md px-2 py-0.5 text-xs"
            >{category}</span
        >
    </div>

    <div class="font-medium mb-1 mt-2">Required:</div>
    <div class="border-l-2 {borderColor} px-2 py-0.5 italic">
        "{requirement}"
    </div>
    {#if candidate_fact !== null}
        <div class="font-medium mb-1 mt-2">Actual:</div>
        <div class="border-l-2 {borderColor} px-2 py-0.5 italic">
            "{candidate_fact}"
        </div>
    {/if}
    <p class="mt-2">{summary}</p>
</div> -->

<div class="rounded-lg shadow-md border border-slate-200 overflow-hidden mb-4 dark:border-gray-600">
    <div class="p-4 rounded-t-lg {style}">
        <h1 class="text-lg font-bold">{title}</h1>
        <p class="text-sm font-light">{category}</p>
    </div>

    <div class="p-4 bg-white dark:bg-gray-800">
        <div>
            <h3 class="font-semibold text-gray-800 dark:text-gray-200">Summary</h3>
            <p class="text-sm text-gray-700 dark:text-gray-100">
                {summary}
            </p>
        </div>

        <div class="mt-4">
            <h3 class="font-semibold text-gray-800 dark:text-gray-200">Requirement</h3>
            <blockquote
                class="mt-1 pl-3 text-sm italic border-l-4 border-gray-300"
            >
                <p class="text-gray-700 dark:text-gray-100">
                    "{requirement}"
                </p>
            </blockquote>
        </div>

        {#if candidate_fact !== null}
            <div class="mt-4">
                <h3 class="font-semibold text-gray-800 dark:text-gray-200">Actual</h3>
                <blockquote
                    class="mt-1 pl-3 text-sm italic border-l-4 border-gray-300"
                >
                    <p class="text-gray-700 dark:text-gray-100">
                        "{candidate_fact}"
                    </p>
                </blockquote>
            </div>
        {/if}
    </div>
</div>
