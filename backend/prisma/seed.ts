import { PrismaClient } from '@prisma/client';
import { faker } from '@faker-js/faker/locale/en';

const db = new PrismaClient();

async function main() {
  // 3 companies, each with a lead & deal
  for (let i = 0; i < 3; i++) {
    const company = await db.company.create({
      data: { name: faker.company.name(), website: faker.internet.url() },
    });

    const lead = await db.lead.create({
      data: {
        email: faker.internet.email(),
        firstName: faker.person.firstName(),
        lastName: faker.person.lastName(),
        phone: faker.phone.number(),
        companyId: company.id,
      },
    });

    await db.deal.create({
      data: {
        title: `New deal with ${company.name}`,
        value: faker.number.int({ min: 500, max: 10000 }),
        companyId: company.id,
      },
    });

    await db.task.create({
      data: {
        title: 'Follow-up call',
        dueDate: faker.date.soon(),
        leadId: lead.id,
      },
    });
  }
}

main().then(() => db.$disconnect()); 