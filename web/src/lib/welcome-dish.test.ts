import { describe, expect, it } from "vitest";
import { pickWelcomeDish } from "./welcome-dish";

describe("pickWelcomeDish", () => {
  it("returns the first dish for index 0", () => {
    expect(pickWelcomeDish(0)).toBe("Spaghetti Aglio e Olio");
  });

  it("cycles through dishes", () => {
    expect(pickWelcomeDish(1)).toBe("Miso Butter Ramen");
    expect(pickWelcomeDish(2)).toBe("Smoked Tomato Risotto");
    expect(pickWelcomeDish(4)).toBe("Spaghetti Aglio e Olio");
  });
});
