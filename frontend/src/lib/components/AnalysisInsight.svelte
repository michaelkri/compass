<script>
    let { title, category, requirement, candidate_fact, summary } = $props();

    // set color based on category
    let backgroundColor;
    let borderColor;
    let textColor;

    switch (category) {
        case "Match":
            backgroundColor = "bg-green-100";
            borderColor = "border-green-400";
            textColor = "text-green-800";
            break;
        case "Missing":
            backgroundColor = "bg-red-100";
            borderColor = "border-red-400";
            textColor = "text-red-800";
            break;
        case "Partial":
            backgroundColor = "bg-yellow-100";
            borderColor = "border-yellow-400";
            textColor = "text-yellow-800";
            break;
        case "Exceeding":
            backgroundColor = "bg-purple-100";
            borderColor = "border-purple-400";
            textColor = "text-purple-800";
            break;
        case "Quick Learn":
            backgroundColor = "bg-blue-100";
            borderColor = "border-blue-400";
            textColor = "text-blue-800";
            break;
        default:
            backgroundColor = "bg-gray-100";
            borderColor = "border-gray-400";
            textColor = "text-gray-800";
    }
</script>

<div class="p-4 {backgroundColor} {borderColor} {textColor} border-2 mb-4 rounded-lg">
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
</div>
