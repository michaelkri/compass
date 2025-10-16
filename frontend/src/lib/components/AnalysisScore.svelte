<script>
    let { score, summary } = $props();

    let textColor, barColor;
    if (score >= 85) {
        textColor = "text-emerald-900";
        barColor = "bg-emerald-800";
    }
    else if (score >= 70) {
        textColor = "text-green-700";
        barColor = "bg-green-600";
    }
    else if (score >= 50) {
        textColor = "text-amber-600";
        barColor = "bg-amber-500";
    }
    else if (score >= 25) {
        textColor = "text-amber-800";
        barColor = "bg-amber-700";
    }
    else {
        textColor = "text-red-800";
        barColor = "bg-red-700";
    }
</script>

<div class="p-5 bg-white rounded-lg shadow-md border border-slate-200">
    <div class="flex justify-between items-baseline">
        <h2 class="text-lg font-bold text-slate-800">Overall Score</h2>
        <span class="text-3xl font-bold {textColor}"
            >{score}<span class="text-lg text-slate-500">/100</span></span
        >
    </div>

    <div class="w-full bg-slate-200 rounded-full h-2.5 mt-2">
        <div class="{barColor} h-2.5 rounded-full" style="width: {score}%"></div>
    </div>

    <div class="mt-4">
        <p class="mt-1 text-md text-slate-600">
            {summary}
        </p>
    </div>
</div>
