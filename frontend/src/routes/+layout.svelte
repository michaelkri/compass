<script lang="ts">
	import '$lib/app.css';
	import favicon from '$lib/assets/favicon.svg';
    import TopBar from '$lib/components/TopBar.svelte';
	
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<title>Compass</title>
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com">
	<link
		href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap"
		rel="stylesheet">
	<link rel="stylesheet" href="/style.css" />
	<style>
		body {
			font-family: 'Inter', sans-serif;
		}
	</style>
</svelte:head>

<div class="flex flex-col h-screen">
	<TopBar />
	{@render children?.()}
</div>
