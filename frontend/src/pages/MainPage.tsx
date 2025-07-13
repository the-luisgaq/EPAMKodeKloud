import css from "./MainPage.module.scss";
import { DataColumnProps, useArrayDataSource } from "@epam/uui-core";
import { Panel, RichTextView, IconContainer, DataTable, Text } from "@epam/uui";
import { default as UuiPromoImage } from "../icons/uui-promo-image.svg?react";
import { useEffect, useMemo, useState } from "react";

const links = [
  {
    label: "UUI docs: ",
    link: "https://uui.epam.com",
    linkLabel: "uui.epam.com",
  },
  {
    label: "Git: ",
    link: "https://github.com/epam/uui",
    linkLabel: "github.com/epam/uui",
  },
];

interface Student {
  [key: string]: any;
}

export const MainPage = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [tableState, setTableState] = useState({});

  useEffect(() => {
    fetch("/report/data")
      .then((r) => r.json())
      .then(setStudents)
      .catch(console.error);
  }, []);

  const dataSource = useArrayDataSource<Student, string, unknown>(
    {
      items: students,
      getId: (item) => item.Email,
    },
    [students],
  );

  const view = dataSource.useView(tableState, setTableState, {});

  const columns: DataColumnProps<Student>[] = useMemo(
    () => [
      {
        key: "Name",
        caption: "Name",
        render: (item) => <Text>{item["Name"]}</Text>,
        width: 150,
      },
      {
        key: "Email",
        caption: "Email",
        render: (item) => <Text>{item["Email"]}</Text>,
        width: 200,
      },
      {
        key: "Program",
        caption: "Program",
        render: (item) => <Text>{item["Program"]}</Text>,
        width: 120,
      },
      {
        key: "Lessons Completed",
        caption: "Lessons",
        render: (item) => <Text>{item["Lessons Completed"]}</Text>,
        width: 80,
      },
      {
        key: "Video Hours Watched",
        caption: "Video Hours",
        render: (item) => <Text>{item["Video Hours Watched"]}</Text>,
        width: 80,
      },
      {
        key: "Labs Completed",
        caption: "Labs",
        render: (item) => <Text>{item["Labs Completed"]}</Text>,
        width: 80,
      },
      {
        key: "License Accepted",
        caption: "License",
        render: (item) => <Text>{item["License Accepted"]}</Text>,
        width: 80,
      },
      {
        key: "Status",
        caption: "Status",
        render: (item) => <Text>{item["Status"]}</Text>,
        grow: 1,
      },
    ],
    [],
  );

  return (
    <main>
      <div className={css.bgImg}>
        <IconContainer icon={UuiPromoImage} />
      </div>
      <Panel cx={css.mainPanel}>
        <RichTextView size="14">
          <h3 className={css.welcome}>Welcome to UUI template app</h3>
          {links.map((value) => (
            <p key={value.label}>
              {value.label}
              <a href={value.link}>{value.linkLabel}</a>
            </p>
          ))}
        </RichTextView>
      </Panel>
      <Panel shadow background="surface-main" cx={css.mainPanel}>
        <DataTable
          {...view.getListProps()}
          getRows={view.getVisibleRows}
          value={tableState}
          onValueChange={setTableState}
          columns={columns}
          headerTextCase="upper"
        />
      </Panel>
    </main>
  );
};
