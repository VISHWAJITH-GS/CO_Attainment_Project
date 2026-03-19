import { ChevronDown, SlidersHorizontal } from "lucide-react";
import { Button } from "../ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Input } from "../ui/input";
import { useEffect, useState } from "react";

const emptyValues = {
  ep: "",
  constraint: "",
  ela: {
    CO1: "",
    CO2: "",
    CO3: "",
    CO4: "",
    CO5: "",
    CO6: "",
  },
};

export default function ParameterSection({ isOpen, completed, onComplete, onToggle, initialValues }) {
  const [values, setValues] = useState(emptyValues);

  useEffect(() => {
    if (!initialValues || Object.keys(initialValues).length === 0) {
      return;
    }

    setValues({
      ep: initialValues.ep || "",
      constraint: initialValues.constraint || "",
      ela: {
        CO1: initialValues?.ela?.CO1 || "",
        CO2: initialValues?.ela?.CO2 || "",
        CO3: initialValues?.ela?.CO3 || "",
        CO4: initialValues?.ela?.CO4 || "",
        CO5: initialValues?.ela?.CO5 || "",
        CO6: initialValues?.ela?.CO6 || "",
      },
    });
  }, [initialValues]);

  return (
    <Card className="border-red-100/80 shadow-[0_16px_35px_-32px_rgba(15,23,42,0.65)]">

      <CardHeader>
        <div className="flex items-center justify-between gap-3">
          <CardTitle className="flex items-center gap-2 text-red-950">
            <SlidersHorizontal size={18} />
            CO Attainment Parameter Section
            {completed && (
              <span className="ml-2 text-xs text-red-900">✔ Completed</span>
            )}
          </CardTitle>
          <Button variant="ghost" size="default" className="h-8 w-8 p-0" onClick={onToggle} aria-label="Toggle parameter section">
            <ChevronDown size={16} className={`transition-transform ${isOpen ? "rotate-180" : "rotate-0"}`} />
          </Button>
        </div>
      </CardHeader>

      {isOpen && (<CardContent className="space-y-5">

        {/* EP and Constraint */}

        <div className="grid gap-4 md:grid-cols-2">

          <div className="space-y-1.5">
            <label className="text-sm font-medium text-slate-700">
              EP Value
            </label>
            <Input
              placeholder="Enter EP Value"
              value={values.ep}
              onChange={(event) =>
                setValues((prev) => ({
                  ...prev,
                  ep: event.target.value,
                }))
              }
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-sm font-medium text-slate-700">
              Constraint Value
            </label>

            <Input
              placeholder="Enter Constraint Value"
              value={values.constraint}
              onChange={(event) =>
                setValues((prev) => ({
                  ...prev,
                  constraint: event.target.value,
                }))
              }
            />
          </div>

        </div>

        {/* ELA Values */}

        <div className="space-y-2">

          <p className="text-sm font-medium text-slate-700">
            ELA Values (CO1 to CO6)
          </p>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">

            {["CO1", "CO2", "CO3", "CO4", "CO5", "CO6"].map((co) => (

              <div key={co} className="space-y-1.5">

                <label className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  {co}
                </label>

                <Input
                  placeholder="ELA"
                  value={values.ela[co]}
                  onChange={(event) =>
                    setValues((prev) => ({
                      ...prev,
                      ela: {
                        ...prev.ela,
                        [co]: event.target.value,
                      },
                    }))
                  }
                />

              </div>

            ))}

          </div>

        </div>
        <div className="pt-3">
        <button
          onClick={() => onComplete?.(values)}
            className="px-4 py-2 bg-red-800 text-white rounded-md hover:bg-red-900"
        >
            Continue
        </button>
        </div>

      </CardContent>)}
    </Card>
  );
}