const categories = [
  { id: 100, parentId: -1, name: "Business", keywords: "Money" },
  { id: 200, parentId: -1, name: "Tutoring", keywords: "Teaching" },
  { id: 101, parentId: 100, name: "Accounting", keywords: "Taxes" },
  { id: 102, parentId: 100, name: "Taxation", keywords: "" },
  { id: 201, parentId: 200, name: "Computer", keywords: "" },
  { id: 103, parentId: 101, name: "Corporate Tax", keywords: "" },
  { id: 202, parentId: 201, name: "Operating System", keywords: "" },
  { id: 109, parentId: 101, name: "Small Business Tax", keywords: "" },
];

function getDetailsForCategory(id) {
  const map = new Map(categories.map(c => [c.id, c]));
  const cat = map.get(id);
  if (!cat) return "Category not found";

  let keywords = cat.keywords;
  let currentParent = cat.parentId;
  while ((!keywords || keywords.trim() === "") && currentParent !== -1) {
    const parentCat = map.get(currentParent);
    if (!parentCat) break;
    if (parentCat.keywords && parentCat.keywords.trim() !== "") {
      keywords = parentCat.keywords;
      break;
    }
    currentParent = parentCat.parentId;
  }

  return `ParentCategoryID=${cat.parentId}, Name=${cat.name}, Keywords=${keywords || ""}`;
}

function getDetailsByLevel(n) {
  const map = new Map();
  categories.forEach(cat => {
    if (!map.has(cat.parentId)) {
      map.set(cat.parentId, []);
    }
    map.get(cat.parentId).push(cat.id);
  });

  let currentLevel = 1;
  let currentIds = map.get(-1) || [];

  while (currentLevel < n) {
    const nextIds = [];
    for (const id of currentIds) {
      const children = map.get(id);
      if (children) nextIds.push(...children);
    }
    currentIds = nextIds;
    currentLevel++;
    if (currentIds.length === 0) break;
  }

  return currentIds;
}

console.time("getDetailsForCategory");
console.log(getDetailsForCategory(201));
console.timeEnd("getDetailsForCategory");
console.log("------------------------------------------------------------------------------");
console.time("getDetailsByLevel");
console.log(getDetailsByLevel(2));
console.timeEnd("getDetailsByLevel");