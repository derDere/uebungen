import { writeFile, mkdir } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';

/**
 * Writes content to the shared data file.
 * @param dataDir - Absolute path to the data directory containing data.txt
 * @param content - The content to write
 */
export async function writeData(dataDir: string, content: string): Promise<void> {
	const filePath = resolve(dataDir, 'data.txt');
	await mkdir(dirname(filePath), { recursive: true });
	await writeFile(filePath, content, 'utf-8');
}
