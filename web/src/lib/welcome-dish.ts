const WELCOME_DISHES = [
  "Spaghetti Aglio e Olio",
  "Miso Butter Ramen",
  "Smoked Tomato Risotto",
  "Harissa Chickpea Bowl",
];

export function pickWelcomeDish(index: number): string {
  return WELCOME_DISHES[index % WELCOME_DISHES.length];
}
