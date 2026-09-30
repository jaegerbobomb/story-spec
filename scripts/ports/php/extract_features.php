#!/usr/bin/env php
<?php

declare(strict_types=1);

/**
 * StorySpec - extract_features.php (PHP port)
 *
 * PHP port of scripts/extract_features.py.
 * Use this if your project already has PHP available.
 * The canonical implementation is the Python version.
 *
 * Usage:
 *   php extract_features.php [options]
 *
 * Options:
 *   --stories-dir=<path>   Source directory (default: stories)
 *   --output-dir=<path>    Output directory (default: tests/features)
 *   --dry-run              Print what would be generated, write nothing
 *   --verbose              Print skipped files too
 */

function resolveArg(string $name, string $default): string
{
    global $argv;
    foreach ($argv as $arg) {
        if (str_starts_with($arg, "--{$name}=")) {
            return substr($arg, strlen("--{$name}="));
        }
    }
    return getcwd() . '/' . $default;
}

$storiesDir = resolveArg('stories-dir', 'stories');
$outputDir  = resolveArg('output-dir', 'tests/features');
$dryRun     = in_array('--dry-run', $argv ?? [], true);
$verbose    = in_array('--verbose', $argv ?? [], true);

exit(main($storiesDir, $outputDir, $dryRun, $verbose));

function main(string $storiesDir, string $outputDir, bool $dryRun, bool $verbose): int
{
    $files = glob($storiesDir . '/S*.md');
    if ($files === false || $files === []) {
        echo "No story files found in {$storiesDir}\n";
        return 0;
    }

    sort($files);
    $generated = $skipped = 0;

    foreach ($files as $file) {
        $content = (string) file_get_contents($file);
        $fm      = parseFrontmatter($content);

        if (($fm['bdd'] ?? 'false') !== 'true') {
            if ($verbose) {
                echo '[skip] ' . basename($file) . " (bdd: false)\n";
            }
            $skipped++;
            continue;
        }

        $id        = $fm['id']    ?? basename($file, '.md');
        $title     = $fm['title'] ?? $id;
        $scenarios = extractScenarios($content);

        if ($scenarios === []) {
            if ($verbose) {
                echo '[skip] ' . basename($file) . " (no scenarios found)\n";
            }
            $skipped++;
            continue;
        }

        $feature = buildFeature($id, $title, $scenarios);
        $out     = $outputDir . '/' . $id . '.feature';

        if ($dryRun) {
            echo "[dry-run] Would generate: {$out}\n";
            if ($verbose) {
                echo $feature . "\n";
            }
        } else {
            if (!is_dir($outputDir)) {
                mkdir($outputDir, 0755, true);
            }
            file_put_contents($out, $feature);
            echo "[ok] {$out}\n";
        }

        $generated++;
    }

    echo "\n{$generated} file(s) generated, {$skipped} skipped.\n";
    return 0;
}

/** @return array<string, string> */
function parseFrontmatter(string $content): array
{
    if (!str_starts_with($content, '---')) {
        return [];
    }
    $end = strpos($content, '---', 3);
    if ($end === false) {
        return [];
    }
    $result = [];
    foreach (explode("\n", substr($content, 3, $end - 3)) as $line) {
        $line = trim($line);
        if ($line === '' || !str_contains($line, ':')) {
            continue;
        }
        [$key, $value] = explode(':', $line, 2);
        $value = trim($value, " \t\r\n\"'");
        if (!str_starts_with($value, '[')) {
            $result[trim($key)] = $value;
        }
    }
    return $result;
}

/**
 * The text under the `## Acceptance Criteria` heading, or null if absent.
 *
 * The heading counts only at the **start of a line**: a story may legitimately
 * mention "## Acceptance Criteria" inside a sentence or a Gherkin step (a story
 * about the extractor itself does), and a plain substring search would then cut
 * the section short at that mention — losing every scenario, silently.
 * Parity with the Python extractor.
 */
function acceptanceCriteriaSection(string $content): ?string
{
    if (!preg_match_all('/^## Acceptance Criteria[ \t]*$/mu', $content, $m, PREG_OFFSET_CAPTURE)) {
        return null;
    }
    foreach ($m[0] as [$heading, $offset]) {
        $rest    = substr($content, $offset + strlen($heading));
        $nextH2  = preg_match('/^## /mu', $rest, $next, PREG_OFFSET_CAPTURE);
        $section = $nextH2 ? substr($rest, 0, $next[0][1]) : $rest;
        if (trim($section) !== '') {
            return $section;
        }
    }
    return null;
}

/** @return list<array{title: string, steps: list<array{keyword: string, text: string}>}> */
function extractScenarios(string $content): array
{
    $section = acceptanceCriteriaSection($content);
    if ($section === null) {
        return [];
    }

    $scenarios = [];
    $current   = null;

    foreach (explode("\n", $section) as $line) {
        if (preg_match('/^###\s+Scenario:\s+(.+)$/u', $line, $m)) {
            if ($current !== null) {
                $scenarios[] = $current;
            }
            $current = ['title' => trim($m[1]), 'steps' => []];
            continue;
        }
        if ($current === null) {
            continue;
        }
        if (preg_match('/^\*\s+\*\*(Given|When|Then|And|But)\*\*\s+(.+)$/u', $line, $m)) {
            $current['steps'][] = ['keyword' => $m[1], 'text' => trim($m[2])];
        }
    }

    if ($current !== null && $current['steps'] !== []) {
        $scenarios[] = $current;
    }
    return $scenarios;
}

/** @param list<array{title: string, steps: list<array{keyword: string, text: string}>}> $scenarios */
function buildFeature(string $id, string $title, array $scenarios): string
{
    $lines = ["Feature: [{$id}] {$title}", ''];
    foreach ($scenarios as $s) {
        $lines[] = "  Scenario: {$s['title']}";
        foreach ($s['steps'] as $step) {
            $lines[] = "    {$step['keyword']} {$step['text']}";
        }
        $lines[] = '';
    }
    return implode("\n", $lines);
}
